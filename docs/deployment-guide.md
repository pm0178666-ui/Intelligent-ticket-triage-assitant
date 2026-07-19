# Deployment Guide

## Overview

The application is deployed using AWS Serverless Application Model (AWS SAM) for backend infrastructure and AWS Amplify Hosting for the React frontend.

The solution consists of a React + Vite frontend application, AWS serverless backend services, Amazon Bedrock AI services, and Amazon Cognito authentication.

---

# Prerequisites

Before deploying the application, ensure the following tools and services are available.

## Software Requirements

- Python 3.11
- Node.js
- npm
- Git
- AWS CLI
- AWS SAM CLI
- Visual Studio Code

---

## AWS Services Required

- Amazon Cognito
- AWS Amplify Hosting
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

# Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure AWS Credentials

Configure AWS CLI:

```bash
aws configure
```

Provide:

- AWS Access Key
- AWS Secret Key
- AWS Region
- Output Format

---

# Build the SAM Application

```bash
sam build
```

AWS SAM packages Lambda functions and validates the infrastructure template.

---

# Deploy Backend Application

Deploy using:

```bash
sam deploy --guided
```

Provide:

- Stack Name
- AWS Region
- Confirm Changes
- IAM Capability

After successful deployment, AWS provisions:

- Amazon API Gateway
- AWS Lambda Functions
- Amazon DynamoDB Tables
- Amazon SQS Queue
- Amazon S3 Bucket
- IAM Roles
- Amazon SES configuration

---

# Deploy React Frontend using AWS Amplify

The frontend application is developed using React with Vite and deployed using AWS Amplify Hosting.

AWS Amplify provides managed hosting, automated builds, HTTPS access, and continuous deployment from the source repository.

---

## Build Frontend Locally

Navigate to the frontend directory:

```bash
cd TicketTriageUI
```

Install frontend dependencies:

```bash
npm install
```

Create production build:

```bash
npm run build
```

---

## Configure AWS Amplify Hosting

1. Connect the GitHub repository to AWS Amplify Hosting.

2. Configure the build settings for the React + Vite application.

3. Add the required frontend environment variables:

```env
VITE_API_URL=https://your-api-id.execute-api.us-east-1.amazonaws.com/Prod
VITE_COGNITO_USER_POOL_ID=us-east-1_xxxxxxxxx
VITE_COGNITO_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
VITE_AWS_REGION=us-east-1
```

4. Start the deployment.

AWS Amplify automatically performs:

- Installing frontend dependencies
- Running the React + Vite build process
- Deploying the frontend application
- Providing secure HTTPS hosting

The deployed React application communicates with backend REST APIs through Amazon API Gateway using authenticated requests with Amazon Cognito JWT tokens.

---

# Configure Amazon Cognito

Create a Cognito User Pool.

Create two User Groups:

- CUSTOMER
- SUPPORT

Create application users and assign them to the appropriate group.

Configure the React frontend with:

- Cognito User Pool ID
- Cognito App Client ID
- AWS Region

These values are stored as frontend environment variables.

Cognito provides:

- User authentication
- JWT token generation
- Role-based access control
- Secure API authorization

---

# Configure Amazon Bedrock

Enable access to the required foundation model.

Update the Processor Lambda environment variables if required.

Verify:

- Model access permissions
- Lambda IAM permissions
- Bedrock invocation configuration

---

# Configure Amazon Bedrock Knowledge Base

Create a Knowledge Base.

Configure:

- Amazon S3 as the document source
- Document synchronization

Update the Processor Lambda with the Knowledge Base ID.

---

# Configure Amazon Bedrock Agent

Create a Bedrock Agent.

Create Action Groups for:

- Get Order Status
- Issue Refund
- Reset Password

Associate each Action Group with the corresponding Lambda functions.

Update the Processor Lambda with:

- Agent ID
- Agent Alias ID

---

# Configure Amazon SES

Verify the sender email address.

If the AWS account is in SES Sandbox mode:

- Verify recipient email addresses
- Or request SES production access

---

# Run Frontend Locally (Development)

Navigate to frontend directory:

```bash
cd TicketTriageUI
```

Install dependencies:

```bash
npm install
```

Start React development server:

```bash
npm run dev
```

The application will be available through the local development server.

---

# Verify the Deployment

Validate the following functionality:

- User login using Amazon Cognito
- Role-based access for CUSTOMER and SUPPORT users
- Ticket creation
- Attachment upload
- Ticket retrieval
- AI ticket classification
- Priority and sentiment analysis
- Knowledge Base responses
- Bedrock Agent actions
- Password reset workflow
- Approval workflow
- Dashboard updates

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
- Lambda permissions

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
- Cognito JWT validation
- CORS configuration

---

## Amplify Deployment Errors

Check:

- AWS Amplify build logs
- Node.js version
- npm dependencies
- Environment variables
- Build configuration

---

# Deployment Architecture

The deployment consists of two parts:

## Frontend

- AWS Amplify Hosting
- React + Vite Application
- Amazon Cognito Authentication

## Backend

- Amazon API Gateway
- AWS Lambda Functions
- Amazon DynamoDB Tables
- Amazon S3 Bucket
- Amazon SQS Queue
- Amazon Bedrock
- Amazon Bedrock Knowledge Base
- Amazon Bedrock Agent
- Amazon SNS
- Amazon SES
- AWS IAM

---

# Conclusion

Following this guide deploys the AI Ticket Triage Assistant as a fully serverless application on AWS.

The deployed solution provides:

- Secure authentication using Amazon Cognito
- React-based user interface hosted on AWS Amplify
- AI-powered ticket processing using Amazon Bedrock
- Knowledge retrieval using Bedrock Knowledge Base
- Automated workflows using Bedrock Agents
- Scalable backend processing using AWS serverless services

The architecture enables a secure, scalable, and maintainable AI-powered ticket management platform.