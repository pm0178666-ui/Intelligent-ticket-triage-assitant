# Deployment Guide

## Overview

This document provides the deployment steps for the AI Ticket Triage Assistant. The application is deployed using AWS Serverless Application Model (AWS SAM) and consists of a Streamlit frontend, AWS serverless backend, Amazon Bedrock AI services, and Amazon Cognito for authentication.

---

# Prerequisites

Before deploying the application, ensure the following tools and services are available.

## Software Requirements

- Python 3.11
- Git
- AWS CLI
- AWS SAM CLI
- Visual Studio Code
- Streamlit

---

## AWS Services Required

- Amazon Cognito
- Amazon API Gateway
- AWS Lambda
- Amazon DynamoDB
- Amazon S3
- Amazon SQS
- Amazon Bedrock
- Amazon Bedrock Knowledge Base
- Amazon Bedrock Agent
- Amazon SES
- AWS IAM

---

# Clone the Repository

```bash
git clone https://github.com/pm0178666-ui/Intelligent-ticket-triage-assitant.git

cd Intelligent-ticket-triage-assistant
```

---

# Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure AWS Credentials

Configure AWS CLI.

```bash
aws configure
```

Provide:

- AWS Access Key
- AWS Secret Key
- Region
- Output Format

---

# Build the SAM Application

```bash
sam build
```

AWS SAM packages all Lambda functions and validates the template.

---

# Deploy the Application

Deploy using:

```bash
sam deploy --guided
```

Provide:

- Stack Name
- AWS Region
- Confirm Changes
- IAM Capability

After deployment, AWS creates:

- API Gateway
- Lambda Functions
- DynamoDB Tables
- SQS Queue
- S3 Bucket
- IAM Roles
- Amazon SES configuration

---

# Configure Amazon Cognito

Create a User Pool.

Create two User Groups.

- Customer
- Support

Create application users and assign them to the appropriate group.

Update the frontend with:

- User Pool ID
- App Client ID
- Region

---

# Configure Amazon Bedrock

Enable access to the required foundation model.

Update the Processor Lambda environment variables if necessary.

---

# Configure Amazon Bedrock Knowledge Base

Create a Knowledge Base.

Configure:

- Amazon S3 as the document source.
- Sync documents.

Update the Processor Lambda with the Knowledge Base ID.

---

# Configure Amazon Bedrock Agent

Create a Bedrock Agent.

Create Action Groups for:

- Get Order Status
- Issue Refund
- Reset Password

Associate each Action Group with its corresponding Lambda function.

Update the Processor Lambda with:

- Agent ID
- Agent Alias ID

---

# Configure Amazon SES

Verify the sender email address.

If the AWS account is in SES Sandbox mode:

- Verify recipient email addresses.
- Or request production access.

---

# Run the Frontend

Navigate to the frontend directory.

Start Streamlit.

```bash
streamlit run app.py
```

Open the application in your browser.

---

# Verify the Deployment

Validate the following functionality:

- User login using Amazon Cognito.
- Ticket creation.
- Attachment upload.
- Ticket retrieval.
- AI ticket analysis.
- Knowledge Base responses.
- Agent action execution.
- Password reset email delivery.
- Approval workflow.
- Dashboard updates.

---

# Troubleshooting

## Lambda Errors

Check:

- Amazon CloudWatch Logs
- IAM permissions
- Environment variables

---

## Bedrock Errors

Verify:

- Model access
- Agent configuration
- Knowledge Base synchronization

---

## SES Errors

Check:

- Verified sender email
- Sandbox restrictions
- Recipient verification

---

## API Errors

Verify:

- API Gateway deployment
- Lambda integration
- Cognito authentication

---

# Deployment Architecture

The deployment provisions:

- Amazon API Gateway
- AWS Lambda Functions
- Amazon DynamoDB Tables
- Amazon S3 Bucket
- Amazon SQS Queue
- Amazon Cognito
- Amazon Bedrock
- Amazon Bedrock Knowledge Base
- Amazon Bedrock Agent
- Amazon SES

---

# Conclusion

Following this guide deploys the AI Ticket Triage Assistant as a fully serverless application on AWS. The deployed solution provides secure authentication, AI-powered ticket processing, knowledge retrieval, and automated operational workflows while leveraging managed AWS services for scalability and maintainability.