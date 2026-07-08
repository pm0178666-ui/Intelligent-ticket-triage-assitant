# AWS Services Used

## Overview

The AI Ticket Triage Assistant is built using a serverless architecture on Amazon Web Services (AWS). Each AWS service is responsible for a specific function within the application, enabling scalability, security, reliability, and intelligent ticket processing.

This document describes the purpose, role, and benefits of each AWS service used in the project.

---

# 1. Amazon Cognito

## Purpose

Amazon Cognito provides secure user authentication and authorization for the application.

## Role in the Project

- Authenticates users during login.
- Manages user accounts and credentials.
- Generates JWT tokens after successful authentication.
- Implements role-based access control using Cognito User Groups.

## User Groups

- Customer
- Support

Customers can access ticket creation and tracking features, while Support users can access administrative dashboards and ticket management features.

## Benefits

- Secure authentication
- Managed identity service
- JWT-based authorization
- Role-based access control
- Reduced authentication management overhead

---

# 2. Amazon API Gateway

## Purpose

Amazon API Gateway serves as the secure entry point for all frontend requests.

## Role in the Project

- Receives HTTP requests from the Streamlit application.
- Routes requests to AWS Lambda functions.
- Handles REST API communication.
- Provides a scalable interface between the frontend and backend.

## Benefits

- Fully managed API service
- Secure request handling
- Automatic scaling
- Easy integration with Lambda

---

# 3. AWS Lambda

## Purpose

AWS Lambda executes the backend business logic without requiring server management.

## Role in the Project

The application uses multiple Lambda functions.

### Ticket Ingestion Lambda

Responsibilities include:

- Validating ticket requests
- Generating Ticket IDs
- Creating pre-signed S3 URLs
- Storing ticket metadata
- Sending processing requests to Amazon SQS

### Ticket Processor Lambda

Responsibilities include:

- Reading messages from Amazon SQS
- Invoking Amazon Bedrock
- Updating ticket information
- Triggering Bedrock Agent workflows

### Lambda Action Group Functions

Used by Amazon Bedrock Agents to execute business operations such as:

- Get Order Status
- Issue Refund
- Reset Password

## Benefits

- Serverless execution
- Automatic scaling
- Pay-per-use pricing
- Event-driven processing

---

# 4. Amazon SQS

## Purpose

Amazon Simple Queue Service (SQS) enables asynchronous communication between application components.

## Role in the Project

Instead of performing AI analysis immediately after ticket creation, ticket requests are placed into an SQS queue.

The Processor Lambda retrieves messages from the queue and processes them independently.

## Benefits

- Decouples application components
- Improves scalability
- Prevents request timeouts
- Reliable message delivery
- Fault tolerance

---

# 5. Amazon DynamoDB

## Purpose

Amazon DynamoDB stores structured ticket information.

## Role in the Project

The database stores:

- Ticket ID
- Subject
- Description
- Customer Information
- Ticket Status
- Category
- Priority
- Sentiment
- AI-generated Response
- Processing Results

The application retrieves this information to display dashboards and ticket details.

## Benefits

- Serverless NoSQL database
- Low-latency performance
- Automatic scaling
- High availability

---

# 6. Amazon S3

## Purpose

Amazon Simple Storage Service (Amazon S3) stores application files and knowledge base documents.

## Role in the Project

Amazon S3 is used for:

### Ticket Attachments

Customer-uploaded files are securely stored using pre-signed URLs.

### Knowledge Base Documents

Documents used by Amazon Bedrock Knowledge Base are stored in S3 for Retrieval-Augmented Generation (RAG).

## Benefits

- Highly durable storage
- Secure file uploads
- Unlimited scalability
- Cost-effective object storage

---

# 7. Amazon Bedrock

## Purpose

Amazon Bedrock provides the Generative AI capabilities of the application.

## Role in the Project

Amazon Bedrock performs AI analysis on submitted tickets.

The AI model is responsible for:

- Ticket classification
- Priority detection
- Sentiment analysis
- Draft response generation

These results are stored in DynamoDB and displayed in the application dashboards.

## Benefits

- Managed foundation models
- No infrastructure management
- Easy integration with AWS services
- AI-powered ticket analysis

---

# 8. Amazon Bedrock Knowledge Base

## Purpose

Amazon Bedrock Knowledge Base enables Retrieval-Augmented Generation (RAG).

## Role in the Project

Knowledge Base retrieves relevant information from documents stored in Amazon S3 before generating responses.

This ensures that AI-generated answers are based on organizational knowledge instead of relying solely on the foundation model.

## Benefits

- Accurate responses
- Reduced hallucinations
- Context-aware information retrieval
- Centralized knowledge management

---

# 9. Amazon Bedrock Agent

## Purpose

Amazon Bedrock Agent enables intelligent workflow automation.

## Role in the Project

The agent determines whether a user request requires:

- Knowledge retrieval
- Business operation execution

When an operational task is required, the agent invokes the appropriate Lambda Action Group.

Implemented action groups include:

- Get Order Status
- Issue Refund
- Reset Password

## Benefits

- Intelligent decision making
- Workflow automation
- Tool invocation
- Reduced manual effort

---

# 10. Amazon SNS

## Purpose

Amazon Simple Notification Service (SNS) delivers notifications for password reset operations.

## Role in the Project

When the Bedrock Agent invokes the Reset Password action group, the corresponding Lambda function publishes a notification through Amazon SNS.

Amazon SNS sends the password reset email to the user, completing the workflow.

## Benefits

- Managed messaging service
- Reliable email delivery
- Event-driven notifications
- Easy integration with Lambda

---

# 11. AWS SAM

## Purpose

AWS Serverless Application Model (SAM) is used to define and deploy the serverless infrastructure.

## Role in the Project

AWS SAM manages deployment of:

- AWS Lambda Functions
- Amazon API Gateway
- Amazon DynamoDB
- Amazon SQS
- Amazon S3
- IAM Roles
- Amazon SNS

Infrastructure is defined as code using the `template.yaml` file.

## Benefits

- Infrastructure as Code (IaC)
- Repeatable deployments
- Simplified serverless application management
- Easy environment provisioning

---

# 12. AWS IAM

## Purpose

AWS Identity and Access Management (IAM) controls permissions between AWS services.

## Role in the Project

IAM roles and policies grant secure access for:

- Lambda to DynamoDB
- Lambda to S3
- Lambda to Amazon Bedrock
- Lambda to SQS
- Lambda to SNS

The application follows the principle of least privilege by assigning only the permissions required for each service.

## Benefits

- Fine-grained access control
- Secure service communication
- Least-privilege security model
- Centralized permission management

---

# Summary

The AI Ticket Triage Assistant leverages a combination of AWS serverless, storage, AI, security, and messaging services to build a scalable and intelligent support automation platform.

Each AWS service has a well-defined responsibility, enabling the application to remain modular, secure, cost-efficient, and easy to maintain while providing AI-powered ticket analysis and automated support workflows.