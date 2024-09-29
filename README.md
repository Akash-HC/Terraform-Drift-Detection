# Terraform Migration & Drift Detection Automation with Python, Jenkins, and Cron Job
## Project Overview:
This project implements a fully automated Terraform drift detection system for AWS infrastructure. The solution is built using Terraform for infrastructure as code (IaC), Jenkins for CI/CD pipeline integration, and a Python script to detect infrastructure drift. The project replaces traditional AWS services such as Lambda and SNS for notification and drift handling, instead using a local cron job and Python script to trigger Jenkins jobs for infrastructure remediation.

The goal of this project is to ensure that the AWS infrastructure remains aligned with the defined Terraform configurations, preventing manual changes from causing discrepancies and improving security, cost efficiency, and operational reliability.
