# Project Flow

## Overview

The AI Ticket Triage Assistant is an intelligent, serverless ticket management system built on AWS. It streamlines customer support by automating ticket submission, AI-based ticket analysis, knowledge retrieval, and support workflows. The application integrates Amazon Bedrock, Amazon Bedrock Knowledge Base, and Amazon Bedrock Agents to provide intelligent responses while leveraging AWS serverless services for scalability and reliability.

---

# End-to-End Project Workflow

The complete workflow consists of the following stages:

1. User Authentication
2. Ticket Creation
3. Attachment Upload
4. Ticket Storage
5. Asynchronous Ticket Processing
6. AI-Based Ticket Analysis
7. Knowledge Base Retrieval
8. Agent-Based Task Automation
9. Dashboard Updates
10. Password Reset Notification

---

# 1. User Authentication

Users access the application through the Streamlit web interface.

Authentication is handled using Amazon Cognito, where users log in using their registered credentials. Based on the assigned Cognito User Group, users receive role-based access to the application.

Supported roles include:

- Customer
- Support Team

Customers can create and monitor their own tickets, while support users have access to dashboards for ticket management, approvals, and order-related operations.

---

# 2. Ticket Creation

After successful authentication, customers can create a new support ticket by providing:

- Subject
- Description
- Category (if applicable)
- Optional attachment

Once the user submits the form, the request is sent to the backend through Amazon API Gateway.

---

# 3. Attachment Upload

If the ticket contains an attachment, the backend generates a pre-signed Amazon S3 URL.

The attachment is securely uploaded to the configured S3 bucket without exposing storage credentials to the client.

This approach improves security while supporting scalable file uploads.

---

# 4. Ticket Storage

The Ticket Ingestion Lambda function performs the following tasks:

- Generates a unique Ticket ID
- Validates the request
- Stores ticket metadata in Amazon DynamoDB
- Uploads attachment metadata
- Places a processing request into Amazon SQS

At this stage, the ticket status is initialized and stored for further processing.

---

# 5. Asynchronous Ticket Processing

Amazon SQS acts as a buffering layer between ticket submission and AI processing.

The Processor Lambda continuously consumes messages from the queue.

Using asynchronous processing prevents delays in the user interface and enables the system to process multiple tickets efficiently.

---

# 6. AI-Based Ticket Analysis

The Processor Lambda invokes Amazon Bedrock to analyze the ticket.

The AI model performs several tasks, including:

- Ticket categorization
- Priority identification
- Sentiment analysis
- Draft response generation

The generated results are written back to Amazon DynamoDB, ensuring that the latest ticket information is available to users and support engineers.

---

# 7. Knowledge Base Retrieval

For informational queries, Amazon Bedrock Knowledge Base retrieves relevant content from documents stored in Amazon S3.

Instead of generating responses solely from the language model, the system performs Retrieval-Augmented Generation (RAG), ensuring that answers are grounded in organizational knowledge.

This improves response accuracy while reducing hallucinations.

---

# 8. Agent-Based Task Automation

The application uses Amazon Bedrock Agents to automate predefined operational tasks.

When a user request requires an action instead of informational retrieval, the agent invokes the appropriate Lambda action group.

Implemented action groups include:

- Get Order Status
- Issue Refund
- Reset Password

Each action group executes the required business logic and returns the result to the user.

---

# 9. Dashboard Updates

Once processing is complete, the updated ticket information becomes available through the application dashboards.

Customers can:

- View submitted tickets
- Track ticket status
- Review ticket details

Support users can:

- Monitor all tickets
- Manage approvals
- Access order management dashboards
- Review AI-generated analysis

---

# 10. Password Reset Notification

For password reset requests, the Bedrock Agent invokes the Reset Password action.

The associated Lambda function triggers Amazon SNS to send the password reset notification email.

This completes the automated password reset workflow without manual intervention.

---

# Summary

The AI Ticket Triage Assistant combines AWS serverless services with Generative AI to automate ticket management from submission to resolution.

By integrating Amazon Bedrock, Knowledge Bases, Bedrock Agents, Amazon SQS, Amazon DynamoDB, Amazon S3, and Amazon Cognito, the system provides an intelligent, scalable, and secure support solution capable of handling both informational and action-based customer requests.