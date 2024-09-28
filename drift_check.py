#!/usr/bin/env python3

import os
import subprocess
import requests
import logging
from requests.auth import HTTPBasicAuth
from datetime import datetime

# Configure Logging
LOG_FILE = os.getenv('LOG_FILE', 'drift_check.log') # mention the path to log file
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Jenkins Configuration
# declare all the environment variables
JENKINS_URL = os.getenv('JENKINS_URL')
JENKINS_USER = os.getenv('JENKINS_USER')
JENKINS_TOKEN = os.getenv('JENKINS_TOKEN') # or you can hardcode the jenkins api
JENKINS_JOB_NAME = os.getenv('JENKINS_JOB_NAME')

# Validate Environment Variables
required_vars = ['JENKINS_URL', 'JENKINS_USER', 'JENKINS_TOKEN', 'JENKINS_JOB_NAME']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    logging.error(f"Missing environment variables: {', '.join(missing_vars)}")
    exit(1)

JENKINS_JOB_URL = f"{JENKINS_URL}/job/{JENKINS_JOB_NAME}/build"
JENKINS_CRUMB_URL = f"{JENKINS_URL}/crumbIssuer/api/json"

def run_subprocess(command, cwd=None):
    """
    Runs a subprocess command and returns the result.
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=cwd,
            check=True
        )
        logging.info(f"Command '{' '.join(command)}' executed successfully.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command {' '.join(command)}: {e.stderr}")
        raise

def get_jenkins_crumb():
    """
    Fetches the Jenkins crumb for CSRF protection.
    """
    try:
        response = requests.get(
            JENKINS_CRUMB_URL,
            auth=HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN)
        )
        response.raise_for_status()
        crumb_data = response.json()
        crumb = crumb_data['crumb']
        crumb_field = crumb_data['crumbRequestField']
        logging.info("Successfully fetched Jenkins crumb.")
        return crumb, crumb_field
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get Jenkins crumb: {e}")
        return None, None

def trigger_jenkins_job():
    """
    Triggers the Jenkins job using the API.
    """
    crumb, crumb_field = get_jenkins_crumb()
    if not crumb or not crumb_field:
        logging.error("Cannot trigger Jenkins job without crumb.")
        return False

    headers = {crumb_field: crumb}
    try:
        response = requests.post(
            JENKINS_JOB_URL,
            auth=HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN),
            headers=headers
        )
        if response.status_code in [200, 201, 202]:
            logging.info(f"Jenkins job '{JENKINS_JOB_NAME}' triggered successfully.")
            return True
        else:
            logging.error(f"Failed to trigger Jenkins job. Status Code: {response.status_code}, Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Error triggering Jenkins job: {e}")
        return False
    
def run_subprocess(command):
    """
    Helper function to run a subprocess command and return the result.
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            logging.error(f"Error executing command {' '.join(command)}: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout, stderr=result.stderr)
        logging.info(f"Command '{' '.join(command)}' executed successfully.")
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        raise

def check_terraform_drift():
    """
    Runs Terraform commands to check for drift.
    """
    try:
        # Initialize Terraform
        run_subprocess(['terraform', 'init'])

        # Run Terraform Plan
        plan_result = subprocess.run(['terraform', 'plan', '-detailed-exitcode', '-out=tfplan'], capture_output=True, text=True)

        # Log the stdout and stderr from the plan
        logging.info(f"Terraform plan output: {plan_result.stdout}")
        logging.error(f"Terraform plan errors: {plan_result.stderr}")

        # Terraform returns:
        # 0: No changes
        # 1: Error
        # 2: Changes detected
        exit_code = plan_result.returncode

        if exit_code == 0:
            logging.info("No drift detected.")
            return False
        elif exit_code == 2:
            logging.info("Drift detected.")
            return True
        else:
            logging.error(f"Terraform plan failed with exit code {exit_code}.")
            return False
    except Exception as e:
        logging.error(f"Exception during Terraform drift check: {e}")
        return False

def main():
    logging.info("Starting Terraform drift check script.")
    drift_detected = check_terraform_drift()

    if drift_detected:
        logging.info("Initiating Jenkins job trigger due to detected drift.")
        job_triggered = trigger_jenkins_job()
        if job_triggered:
            logging.info("Jenkins job triggered successfully.")
        else:
            logging.error("Failed to trigger Jenkins job.")
    else:
        logging.info("No action required. Exiting script.")

    logging.info("Drift check script completed.")

if __name__ == "__main__":
    main()
