# Architecture and Workflow:
## Terraform with S3 Backend
* The infrastructure's state is stored in an Amazon S3 bucket, which serves as the backend for Terraform.
* This ensures a single source of truth for the infrastructure, making it easier to detect and remediate changes (drift).

## Python-Based Drift Detection
* A custom Python script runs periodically to detect drift by executing terraform plan commands. 
* It parses the output to identify any changes between the current infrastructure state and the desired Terraform configuration.

## Triggering Jenkins Pipeline
* If any drift is detected, the Python script triggers a Jenkins pipeline using an HTTP request.
* This pipeline runs the terraform apply command to automatically fix the infrastructure, ensuring it matches the desired state.

## Local Cron Job for Scheduling
* Instead of using AWS Lambda and SNS for notifications and drift detection, a cron job runs the Python script on a scheduled basis (e.g., daily or weekly).
* This approach simplifies the architecture, reduces costs, and eliminates external dependencies.

# Components Breakdown
## 1. Terraform Configuration
* Terraform configurations define the infrastructure and store the state file in an S3 backend.
* The S3 bucket securely stores the state and is accessible for reading and updating infrastructure states during plan and apply operations.
## 2. Python Script
The Python script is the core of the drift detection system. It performs the following tasks:
* Executes terraform plan to compare the live AWS infrastructure with the desired configuration.
* Parses the Terraform output to determine if there is any drift.
* If drift is detected, it sends a request to the Jenkins server to trigger the terraform apply pipeline for remediation.
* Logs all outputs and actions for tracking and debugging purposes.
## 3. Jenkins Pipeline
* Jenkins is configured to automatically apply infrastructure fixes if drift is detected.
* The pipeline pulls the latest Terraform configuration and runs terraform apply to restore the infrastructure to the desired state.
* Jenkins provides logging and monitoring capabilities, ensuring visibility into all infrastructure changes.
## 4. Cron Job
* The cron job is scheduled to periodically run the Python script. 
* This eliminates the need for AWS Lambda, simplifying the architecture and reducing reliance on external services.

# Benefits of This Architecture
## Cost-Effective: 
* The local implementation using cron jobs reduces dependency on cloud services like Lambda and SNS, thus cutting down operational costs.
## Fully Automated Remediation: 
* Any detected infrastructure drift is immediately rectified through the automated pipeline without manual intervention.
## Modular and Extendable: 
* The solution is modular and can be easily extended to other environments or enhanced with additional features, such as real-time Slack notifications or integration with monitoring tools like Prometheus and Grafana.

# Future Enhancements
## Notification System: 
* Add Slack or email notifications to alert team members when drift is detected and remediation is triggered.
## Monitoring: 
* Integrate monitoring tools such as Prometheus and Grafana for real-time visualization of drift detection metrics.
## Multi-Environment Support: 
* Extend the solution to handle multiple AWS accounts and environments by configuring different state backends and Jenkins pipelines.
  
# Conclusion
## This project demonstrates how to automate drift detection and remediation in a Terraform-managed AWS environment. By utilizing Python, Jenkins, and cron jobs, this architecture provides a cost-effective, fully automated solution to ensure the infrastructure always remains aligned with the desired configuration.

