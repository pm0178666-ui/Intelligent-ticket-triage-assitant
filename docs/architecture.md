# System Architecture

## Overview

The AI Ticket Triage Assistant is built using a serverless, event-driven architecture on Amazon Web Services (AWS). The system combines cloud-native services with Generative AI capabilities to automate ticket management, knowledge retrieval, and operational workflows.

The architecture is designed to be scalable, secure, and cost-efficient by leveraging managed AWS services such as AWS Amplify Hosting, Amazon Cognito, Amazon API Gateway, AWS Lambda, Amazon SQS, Amazon DynamoDB, Amazon S3, Amazon Bedrock, Amazon Bedrock Knowledge Base, Amazon Bedrock Agents, and Amazon SNS.

---

# High-Level Architecture

The application consists of the following layers:

- Presentation Layer
- Authentication Layer
- API Layer
- Processing Layer
- Data Storage Layer
- AI Intelligence Layer
- Automation Layer
- Notification Layer

Each layer is responsible for a specific part of the ticket lifecycle while maintaining loose coupling between system components.

---

# Architecture Diagram


```text
architecture/
└── Architecture.png
```

---

# Presentation Layer

The Presentation Layer provides the user interface through a React application built using Vite and deployed using AWS Amplify Hosting.

The frontend communicates with backend services through REST APIs exposed by Amazon API Gateway.

The application provides role-based dashboards for different types of users.

### Customer Features

- User Login
- Create Ticket
- Upload Attachments
- View My Tickets
- Track Ticket Status
- View Ticket Details


### Support Team Features

- Support Dashboard
- Orders Dashboard
- Approval Dashboard
- Ticket Management
- AI Analysis Review


AWS Amplify provides frontend hosting, build automation, and continuous deployment from the source repository.

---


# Frontend Deployment Architecture

The React frontend is deployed using AWS Amplify Hosting.

Deployment Flow:

Developer
   |
   |
GitHub Repository
   |
   |
AWS Amplify Build Pipeline
   |
   |
React Application Hosting
   |
   |
End Users

---


# Authentication Layer

User authentication and authorization are handled using Amazon Cognito.
The React frontend integrates with Amazon Cognito to authenticate users and obtain JWT tokens required for accessing protected APIs.

Cognito manages:

- User registration
- User login
- Secure authentication
- JWT token generation
- Role-based access control

The application defines separate user groups for Customers and Support users, ensuring that each user can only access the features permitted for their role.

---

# API Layer

Amazon API Gateway acts as the entry point for all authenticated requests from the React frontend application.

Responsibilities include:

- Receiving HTTP requests
- Routing requests to backend Lambda functions
- Handling request validation
- Managing secure API access

This layer provides a secure and scalable interface between the frontend and backend services.

---

# Processing Layer

The backend processing is implemented using AWS Lambda functions.

## Ticket Ingestion Lambda

The Ticket Ingestion Lambda is responsible for:

- Validating incoming ticket requests
- Generating unique Ticket IDs
- Creating pre-signed Amazon S3 URLs
- Storing ticket metadata
- Publishing processing requests to Amazon SQS

This function completes quickly, allowing users to receive an immediate response after ticket submission.

---

## Ticket Processor Lambda

The Processor Lambda is triggered asynchronously by Amazon SQS.

Its responsibilities include:

- Reading ticket information
- Invoking Amazon Bedrock
- Performing AI analysis
- Updating ticket metadata
- Triggering Agent workflows when required

Separating ticket submission from processing improves responsiveness and system scalability.

---

# Data Storage Layer

The application stores data using Amazon DynamoDB and Amazon S3.

## Amazon DynamoDB

DynamoDB stores structured ticket information including:

- Ticket ID
- Subject
- Description
- Category
- Priority
- Sentiment
- Status
- AI-generated response
- Customer information

Its serverless architecture provides low-latency access with automatic scaling.

---

## Amazon S3

Amazon S3 is used for:

- Ticket attachments
- Knowledge Base source documents

The application uploads attachments securely using pre-signed URLs, eliminating direct access to storage resources.

---

# Queue Layer

Amazon SQS enables asynchronous communication between backend services.

Instead of processing AI requests immediately after ticket creation, ticket events are placed into an SQS queue.

The Processor Lambda consumes these messages independently, allowing:

- Better scalability
- Reduced API response time
- Improved fault tolerance
- Reliable message delivery

---

# AI Intelligence Layer

The AI layer is powered by Amazon Bedrock.

Amazon Bedrock performs intelligent analysis of support tickets.

The AI model is responsible for:

- Ticket classification
- Priority prediction
- Sentiment analysis
- Draft response generation

This enables support engineers to receive AI-assisted recommendations while reducing manual effort.

---

# Knowledge Base Layer

The application integrates Amazon Bedrock Knowledge Base to provide Retrieval-Augmented Generation (RAG).

Knowledge Base documents are stored in Amazon S3 and indexed for semantic retrieval.

When users ask informational questions, the system retrieves relevant documentation before generating responses.

Benefits include:

- Context-aware answers
- Reduced hallucinations
- Improved response accuracy
- Centralized organizational knowledge

---

# Agent Automation Layer

Amazon Bedrock Agents enable intelligent task automation.

Instead of only generating responses, the agent can invoke backend business logic through Lambda Action Groups.

Implemented action groups include:

- Get Order Status
- Issue Refund
- Reset Password

The agent determines whether a request requires knowledge retrieval or operational execution before selecting the appropriate workflow.

---

# Notification Layer

Amazon SNS is used for password reset notifications.

When the Bedrock Agent invokes the Reset Password action group, the associated Lambda function publishes a notification through Amazon SNS.

The user receives a password reset email without requiring manual intervention.

---

# End-to-End Request Flow

The request flow follows these steps:

1. User accesses the React application hosted on AWS Amplify.
2. User authenticates through Amazon Cognito.
3. Cognito returns JWT authentication tokens.
4. User submits a support ticket through the React UI.
5. React frontend sends an authenticated request to API Gateway.
6. API Gateway validates the Cognito token.
7. Ticket Ingestion Lambda validates the request.
8. Ticket metadata is stored in DynamoDB.
9. Attachments are uploaded to Amazon S3.
10. A processing message is published to Amazon SQS.
11. Processor Lambda consumes the message.
12. Amazon Bedrock performs AI analysis.
13. Knowledge Base retrieves contextual information when required.
14. Bedrock Agent invokes action groups for operational tasks.
15. Updated ticket information is stored in DynamoDB.
16. React dashboard displays updated ticket status.
17. Password reset requests trigger Amazon SNS notifications.

---

# Scalability

The architecture is designed using serverless AWS services that automatically scale based on workload.

Scalability is achieved through:

- AWS Lambda auto scaling
- Amazon SQS message buffering
- Amazon DynamoDB on-demand capacity
- Amazon S3 unlimited storage
- Amazon Bedrock managed inference

The architecture can support increasing ticket volumes without infrastructure management.

---

# Security

Security is implemented throughout the application.

Key security features include:

- Amazon Cognito authentication
- Role-based authorization
- Secure JWT token validation
- Amplify HTTPS hosted frontend
- Pre-signed Amazon S3 upload URLs
- IAM-based service permissions
- Managed AWS services
- Secure API Gateway endpoints


These mechanisms protect both user data and backend resources.

---

# Architectural Benefits

The implemented architecture provides several advantages:

- Fully serverless infrastructure
- Event-driven processing
- AI-powered ticket analysis
- Intelligent knowledge retrieval
- Automated operational workflows
- Secure authentication
- High scalability
- Low operational overhead
- Cost optimization through managed AWS services
- Modular and extensible design

---

# Conclusion

The AI Ticket Triage Assistant architecture combines modern AWS serverless technologies with Generative AI services to deliver an intelligent, scalable, and secure support automation platform.

The modular design enables future enhancements such as additional AI models, new action groups, advanced analytics, and expanded support workflows without requiring major architectural changes.