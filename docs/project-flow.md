# Project Flow

## Overview

The AI Ticket Triage Assistant is an intelligent, serverless ticket management system built on AWS.

The application streamlines customer support by automating ticket submission, AI-based ticket analysis, knowledge retrieval, and operational workflows.

The solution consists of a React + Vite frontend hosted on AWS Amplify, Amazon Cognito authentication, AWS serverless backend services, Amazon Bedrock AI capabilities, Amazon Bedrock Knowledge Base, and Amazon Bedrock Agents.

The architecture enables secure, scalable, and intelligent ticket processing while reducing manual support effort.

---

# End-to-End Project Workflow

The complete workflow consists of the following stages:

1. User Access Through React Frontend
2. User Authentication
3. Ticket Creation
4. Attachment Upload
5. Ticket Storage
6. Asynchronous Ticket Processing
7. AI-Based Ticket Analysis
8. Knowledge Base Retrieval
9. Agent-Based Task Automation
10. Dashboard Updates
11. Password Reset Notification

---

# 1. User Access Through React Frontend

Users access the application through the React + Vite frontend application deployed using AWS Amplify Hosting.

AWS Amplify provides:

- Frontend hosting
- Automated build and deployment
- HTTPS-based application access
- Continuous deployment from the source repository

The React application communicates with backend services through REST APIs exposed by Amazon API Gateway.

---

# 2. User Authentication

Authentication is handled using Amazon Cognito.

Users log in through the React frontend using their registered credentials.

After successful authentication, Amazon Cognito generates JWT tokens which are attached to API requests.

Amazon API Gateway validates these tokens before forwarding requests to backend Lambda functions.

The application uses Cognito User Groups for role-based access control.

Supported roles include:

- CUSTOMER
- SUPPORT

### CUSTOMER Users

Customers can:

- Create tickets
- Upload attachments
- View their submitted tickets
- Track ticket status
- View ticket details

### SUPPORT Users

Support users can:

- View all tickets
- Manage ticket workflows
- Access approval dashboards
- Review AI-generated analysis
- Manage operational requests

---

# 3. Ticket Creation

After successful authentication, customers can create a support ticket through the React frontend.

Users provide:

- Subject
- Description
- Customer information
- Optional attachment

When the user submits the ticket, the React application sends an authenticated request to Amazon API Gateway.

The Cognito JWT token is included with the request for secure authorization.

API Gateway forwards the request to the Ticket Ingestion Lambda function.

---

# 4. Attachment Upload

If the ticket contains an attachment, the backend generates a pre-signed Amazon S3 URL.

The React frontend uses this URL to upload the file directly to Amazon S3.

This approach provides:

- Secure file upload
- Reduced backend load
- No exposure of AWS credentials
- Scalable storage handling

---

# 5. Ticket Storage

The Ticket Ingestion Lambda performs the following operations:

- Validates incoming ticket requests
- Generates a unique Ticket ID
- Stores ticket metadata in Amazon DynamoDB
- Stores attachment information
- Publishes a processing message to Amazon SQS

At this stage, the ticket is created successfully and marked for AI processing.

---

# 6. Asynchronous Ticket Processing

Amazon SQS acts as a communication layer between ticket submission and AI processing.

The ticket processing request is placed into the SQS queue.

The Processor Lambda consumes messages from the queue and performs AI analysis independently.

This asynchronous design provides:

- Faster user response time
- Improved scalability
- Fault tolerance
- Reliable message processing

---

# 7. AI-Based Ticket Analysis

The Processor Lambda invokes Amazon Bedrock for intelligent ticket analysis.

The AI model performs:

- Ticket classification
- Priority prediction
- Sentiment analysis
- Draft response generation

The generated AI results are stored back into Amazon DynamoDB.

The updated information is later displayed through the React dashboards.

---

# 8. Knowledge Base Retrieval

The application integrates Amazon Bedrock Knowledge Base to provide Retrieval-Augmented Generation (RAG).

Knowledge documents are stored in Amazon S3.

When required, Amazon Bedrock Knowledge Base retrieves relevant information from these documents before generating responses.

This improves:

- Response accuracy
- Context awareness
- Knowledge grounding
- Reduction of AI hallucinations

---

# 9. Agent-Based Task Automation

Amazon Bedrock Agents enable automated execution of operational workflows.

When a request requires an action instead of information retrieval, the Bedrock Agent invokes the appropriate Lambda Action Group.

Implemented action groups include:

- Get Order Status
- Issue Refund
- Reset Password

The agent determines the required workflow and executes the corresponding backend Lambda function.

---

# 10. Dashboard Updates

After AI processing is completed, updated ticket information is stored in DynamoDB.
The React frontend retrieves the latest ticket information through API Gateway APIs.

### CUSTOMER Dashboard

Customers can:

- View submitted tickets
- Track ticket status
- Review ticket details
- View AI-generated responses

### SUPPORT Dashboard

Support users can:

- Monitor all tickets
- Review AI analysis
- Manage approvals
- Access order dashboards
- Handle operational workflows

---

# 11. Password Reset Notification

For password reset requests, the Bedrock Agent invokes the Reset Password action.

The Reset Password Lambda function performs the required operation and publishes notifications using Amazon SNS.

Amazon SNS delivers the password reset notification email to the user.

This completes the automated password reset workflow.

---

# Frontend Deployment Flow

The React frontend deployment workflow follows:

```
Developer
    |
    |
GitHub Repository
    |
    |
AWS Amplify Hosting
    |
    |
React + Vite Application
    |
    |
End Users
```

AWS Amplify automatically performs:

- Dependency installation
- Application build
- Frontend deployment
- HTTPS hosting

---

# Complete System Workflow

The complete request flow is:

```
User
 |
 |
React + Vite Frontend
 |
 |
Amazon Cognito Authentication
 |
 |
API Gateway
 |
 |
Ticket Ingestion Lambda
 |
 |
DynamoDB + S3
 |
 |
Amazon SQS
 |
 |
Processor Lambda
 |
 |
Amazon Bedrock
 |
 |
Knowledge Base / Bedrock Agent
 |
 |
Action Lambda Functions
 |
 |
DynamoDB Update
 |
 |
React Dashboard
```

---

# Summary

The AI Ticket Triage Assistant combines AWS serverless services with Generative AI capabilities to automate the complete ticket lifecycle.

By integrating:

- React + Vite
- AWS Amplify Hosting
- Amazon Cognito
- Amazon API Gateway
- AWS Lambda
- Amazon SQS
- Amazon DynamoDB
- Amazon S3
- Amazon Bedrock
- Amazon Bedrock Knowledge Base
- Amazon Bedrock Agents
- Amazon SNS

the system provides a secure, scalable, and intelligent support automation platform.

The modular architecture enables future enhancements such as additional AI models, new action workflows, advanced analytics, and expanded support capabilities.