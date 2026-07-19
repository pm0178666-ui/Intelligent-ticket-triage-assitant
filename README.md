# Intelligent Ticket Triage Assistant2


![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![AWS](https://img.shields.io/badge/AWS-Serverless-orange?logo=amazonaws)
![Amazon Bedrock](https://img.shields.io/badge/Amazon-Bedrock-FF9900)
![AWS SAM](https://img.shields.io/badge/AWS-SAM-red)
![React](https://img.shields.io/badge/Frontend-React-blue?logo=react)
![Vite](https://img.shields.io/badge/Build-Vite-purple?logo=vite)
![AWS Amplify](https://img.shields.io/badge/AWS-Amplify-orange?logo=awsamplify)
![License](https://img.shields.io/badge/License-Educational-green)


An AI-powered customer support system built using **AWS Serverless, React, and Amazon Bedrock** that automatically classifies support tickets, retrieves knowledge-based answers, performs operational tasks through AI Agents, and manages approval workflows using a Human-in-the-Loop approach.

The project demonstrates modern **Agentic AI architecture** by integrating Amazon Bedrock Agents with AWS serverless services to automate customer support operations while keeping humans involved for sensitive actions such as refunds and password resets.

The frontend application is developed using **React with Vite** and deployed using **AWS Amplify**. User authentication is implemented using **Amazon Cognito**, supporting customer registration, email verification, secure login, and role-based access control.

---

# Project Overview

The Intelligent Ticket Triage Assistant enables customers to raise support tickets through a modern web interface while AI automatically analyzes the request, determines its category and priority, retrieves relevant information from the Knowledge Base, or executes business actions using Amazon Bedrock Agent Action Groups.

The solution is built on a completely serverless AWS architecture and uses Retrieval Augmented Generation (RAG) for answering policy and documentation-related queries.

---

# Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [AWS Services Used](#-aws-services-used)
- [Technology Stack](#️-technology-stack)
- [Project Workflow](#-project-workflow)
- [Project Structure](#-project-structure)
- [Running the Project](#️-running-the-project)
- [Environment Variables](#-environment-variables)
- [Security](#-security)
- [Model Evaluation](#-model-evaluation)
- [Future Enhancements](#-future-enhancements)
- [Demo](#-demo)
- [Screenshots](#-screenshots)
- [Author](#-author)


---

# Features

- Modern React + Vite User Interface
- Frontend deployment using AWS Amplify
- Secure REST API integration
- AI-powered ticket classification
- Automatic priority detection
- Ticket complexity analysis
- Retrieval Augmented Generation (RAG)
- Amazon Bedrock Agent orchestration
- Order Status lookup
- Refund approval workflow
- Password reset workflow
- Human-in-the-loop approvals
- Attachment upload to Amazon S3
- Customer Dashboard
- Support Dashboard
- Customer Sign Up functionality
- Email verification using Amazon Cognito
- Role-based authentication using Amazon Cognito
- Serverless deployment using AWS SAM


---

# Architecture

The application follows an event-driven serverless architecture.

## Architecture Diagram

![AWS Architecture](architecture/Architecture.png)


---

# AWS Services Used

| Service | Purpose |
|----------|----------|
| AWS SAM | Infrastructure as Code |
| API Gateway | REST APIs |
| AWS Lambda | Business Logic |
| Amazon DynamoDB | Ticket & Order Storage |
| Amazon SQS | Asynchronous Processing |
| Amazon S3 | Attachments & Knowledge Base Documents |
| Amazon Bedrock Agent | AI Orchestration |
| Amazon Bedrock Knowledge Base | Retrieval Augmented Generation |
| Amazon Cognito | User Registration, Authentication and Authorization |
| Amazon SNS | Notifications |
| Amazon SES | Password Reset Emails |
| AWS Amplify | React Frontend Hosting & Continuous Deployment |
| IAM | Permissions |

---

# Technology Stack

### Frontend

- React
- Vite
- React Router
- Axios
- CSS
- AWS Amplify Hosting


### Backend

- Python
- AWS Lambda
- AWS SAM
- API Gateway


### AI

- Amazon Bedrock Agent
- Amazon Bedrock Knowledge Base
- Amazon Nova Lite


### Database

- Amazon DynamoDB


### Storage

- Amazon S3


### Authentication

- Amazon Cognito User Pools

---

# Project Workflow

## 1. Infrastructure Deployment

All cloud resources are provisioned using AWS SAM.

Resources include:

- API Gateway
- Lambda Functions
- DynamoDB Tables
- Amazon SQS
- Amazon S3
- Amazon SNS
- IAM Roles

Deployment commands:

```bash
sam build
sam deploy
```

---

## 2. Customer Authentication

Customers authenticate through **Amazon Cognito User Pools**.

Authentication workflow:

- User Sign Up
- Email verification
- Secure Login
- Role-based access control


Role-based access is implemented for:

- Customer
- Support Team

---

## Customer Sign Up Flow

The customer registration process:

```
User Registration
        |
        v
Amazon Cognito Sign Up
        |
        v
Email Verification
        |
        v
Account Activation
        |
        v
Secure Login
```

---

## 3. Ticket Creation

The customer creates a ticket by providing:

- Name
- Email
- Subject
- Description
- Attachment (Optional)

The Ingestion Lambda:

- Generates a unique Ticket ID
- Creates timestamp
- Generates an S3 pre-signed upload URL
- Stores ticket metadata in DynamoDB
- Sends processing request to Amazon SQS

---

## 4. Attachment Upload

Attachments are uploaded directly to Amazon S3 using pre-signed URLs.

Only the object key is stored in DynamoDB.

This minimizes Lambda execution time and supports larger files efficiently.

---

---

## 5. Asynchronous Processing

Instead of directly invoking AI, tickets are pushed into Amazon SQS.

Processor Lambda consumes messages from the queue.

Benefits include:

- Better scalability
- Fault tolerance
- Loose coupling
- Improved reliability

---

## 6. AI Ticket Processing

Processor Lambda invokes Amazon Bedrock Agent.

The agent automatically performs:

- Ticket Classification
- Priority Detection
- Complexity Detection
- Sentiment Analysis
- Customer Response Generation

The processed information is stored back in DynamoDB.

---

## 7. Retrieval Augmented Generation (RAG)

Knowledge documents are stored in Amazon S3 and synchronized with Amazon Bedrock Knowledge Base.

For informational requests, the Bedrock Agent retrieves the most relevant document before generating a response.

Supported knowledge includes:

- Refund Policy
- Password Policy
- Billing Information
- Help Documentation

---

## 8. AI Action Groups

Operational requests are handled using Amazon Bedrock Agent Action Groups.

Implemented tools include:

### Order Status

Retrieves:

- Order Status
- Order Amount


### Approval Workflow

Creates approval requests for:

- Refund Requests
- Password Reset Requests

---

## 9. Human-in-the-Loop Approval

Sensitive operations require manual approval.

Workflow:

```
Customer

↓

Bedrock Agent

↓

Approval Request Lambda

↓

Approvals Table

↓

Support Dashboard

↓

Approve / Reject

↓

Approval Action Lambda

↓

Refund / Password Reset
```

---

## 10. Password Reset

The Reset Password Lambda:

- Retrieves customer email
- Generates reset token
- Creates reset link
- Sends email using Amazon SES
- Updates ticket status

---

## 11. Customer Portal

The React-based customer portal provides:

Features include:

- User Registration
- Email Verification
- User Login
- Create Ticket
- Upload Attachments
- View My Tickets
- Track Ticket Status
- View AI Response
- Ticket Details


---

## 12. Support Portal

Support users can:

- View all tickets
- Monitor dashboards
- Review approvals
- Approve requests
- Reject requests
- Track ticket status

---

# Project Structure

```
Intelligent-ticket-triage-assistant/

├── TicketTriageUI/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── ticket-triage-assistant/
│   ├── ingestion/
│   ├── processor/
│   ├── approval-request/
│   ├── approval-action/
│   ├── issue-refund/
│   ├── reset-password/
│   ├── get-order-status/
│   ├── template.yaml
│   ├── samconfig.toml
│   └── requirements.txt
│
├── evaluation/
│   ├── evaluation_results.csv
│   ├── reports.py
│   ├── evaluation_report.md
│   ├── evaluation_summary.txt
│   └── README.md
│
├── architecture/
│   └── Architecture.png
│
├── screenshots/
│   ├── login.png
│   ├── signup.png
│   ├── customer-dashboard.png
│   ├── create-ticket.png
│   ├── my-tickets-page.png
│   ├── ticket-details-page.png
│   ├── support-home-page.png
│   ├── support-dashboard.png
│   ├── orders-dashboard.png
│   └── approval-dashboard.png
│
├── demo/
│   └── demo.gif
│
├── docs/
│
├── .gitignore
├── .env.example
├── README.md
└── LICENSE
```

---

# Running the Project

## Backend

```bash
cd ticket-triage-assistant

sam build

sam deploy
```

---

## Frontend

```bash
cd TicketTriageUI

npm install

npm run dev
```

---

# Deployment

## Frontend Deployment

The React frontend is deployed using **AWS Amplify Hosting**.

Deployment workflow:

```
GitHub Repository
        |
        v
AWS Amplify Build Pipeline
        |
        v
React Application Deployment
```

AWS Amplify provides:

- Automatic builds
- Continuous deployment from GitHub
- Secure HTTPS hosting
- Managed frontend deployment

Every push to the connected GitHub repository automatically triggers a new build and deployment.

---

## Backend Deployment

The backend infrastructure is deployed using **AWS SAM**.

Deploy using:

```bash
cd ticket-triage-assistant

sam build

sam deploy
```

The backend provisions:

- API Gateway
- AWS Lambda Functions
- Amazon DynamoDB
- Amazon SQS
- Amazon S3
- Amazon SNS
- IAM Roles

---

# Environment Variables

Copy:

```
.env.example
```

to:

```
.env
```

Update the required configuration values before running the application.

---

# Security

- Sensitive credentials are never committed to GitHub.
- AWS Lambda runtime configuration is managed through AWS SAM.
- Environment-specific configuration is stored separately.
- Authentication is handled using Amazon Cognito.
- User registration and login are secured through Cognito User Pools.
- Password reset emails are sent securely through Amazon SES.
- S3 uploads use secure pre-signed URLs.

---

# Model Evaluation

The AI pipeline was evaluated using 50 customer support tickets.

Evaluation metrics:

| Metric | Result |
|---|---:|
| Tickets Evaluated | 50 |
| Processing Success Rate | 100% |
| Category Classification Accuracy | 98% |
| Priority Identification Accuracy | 44% |
| Sentiment Analysis Accuracy | 58% |
| Response Generation Success | 100% |
| Average Processing Latency | 4.57 seconds |
| Fastest Processing Time | 3.87 seconds |
| Maximum Processing Time | 7.58 seconds |

Detailed evaluation documentation is available in:

```
evaluation/
```

---

# Future Enhancements

- Multi-language support
- SLA prediction
- Ticket sentiment analytics
- Automatic ticket routing
- Real-time monitoring dashboard
- Voice-enabled ticket creation
- Multi-model AI comparison
- Continuous AI evaluation pipeline

---

# Demo

### Application Demo

<p align="center">
<img src="demo/demo.gif" width="900">
</p>

---

# Screenshots

## Login

<img src="screenshots/login.png" alt="Login" width="100%">

---

## Sign Up

<img src="screenshots/signup.png" alt="Sign Up" width="100%">

---

## Customer Dashboard

<img src="screenshots/customer-dashboard.png" alt="Customer Dashboard" width="100%">

---

## Create Ticket

<img src="screenshots/create-ticket.png" alt="Create Ticket" width="100%">

---

## My Tickets

<img src="screenshots/my-tickets-page.png" alt="My Tickets Page" width="100%">

---

## Ticket Details

<img src="screenshots/ticket-details-page.png" alt="Ticket Details Page" width="100%">

---

## Support Home Page

<img src="screenshots/support-home-page.png" alt="Support Home Page" width="100%">

---

## Support Dashboard

<img src="screenshots/support-dashboard.png" alt="Support Dashboard" width="100%">

---

## Orders Dashboard

<img src="screenshots/orders-dashboard.png" alt="Orders Dashboard" width="100%">

---

## Approval Dashboard

<img src="screenshots/approval-dashboard.png" alt="Approval Dashboard" width="100%">

---

# Author

**Padmaja**

Developed as an AI-powered serverless customer support solution using AWS, React, and Amazon Bedrock.

---

# License

This project is developed for educational and demonstration purposes.