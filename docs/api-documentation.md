# API Documentation

## Overview

The AI Ticket Triage Assistant exposes RESTful APIs through Amazon API Gateway.
These APIs enable ticket management, approval workflows, and order retrieval.

The React-based frontend application hosted on AWS Amplify consumes these APIs.
Backend AI processing is handled asynchronously using Amazon SQS, AWS Lambda,
and Amazon Bedrock services.

---

# Base URL

```
https://xesajug973.execute-api.us-east-1.amazonaws.com/Prod
```

---

# Authentication

The application uses Amazon Cognito for authentication and authorization.

Users authenticate through the React frontend application using Amazon Cognito.

After successful authentication, Cognito issues JWT tokens which are attached
to API requests made to Amazon API Gateway.

API Gateway validates the token before forwarding requests to backend Lambda functions.

User groups are used for role-based access:

- CUSTOMER
  - Create tickets
  - View own tickets

- SUPPORT
  - View and manage tickets
  - Handle approval workflows

---

# API Endpoints

## 1. Create Ticket

### Endpoint

```
POST /tickets
```

### Description

Creates a new support ticket and queues it for AI processing.

### Request Body

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| subject | String | Yes | Ticket subject |
| description | String | Yes | Issue description |
| customerName | String | Yes | Customer name |
| customerEmail | String | Yes | Customer email |
| attachment | File | No | Optional attachment |

### Success Response

```json
{
    "ticketId": "TKT-10001",
    "status": "Submitted"
}
```

### Status Codes

| Code | Meaning |
|------|----------|
|200|Ticket Created|
|400|Invalid Request|
|500|Internal Server Error|

---

# 2. Get All Tickets

### Endpoint

```
GET /tickets
```

### Description

Retrieves all support tickets stored in the system.

### Success Response

```json
[
    {
        "ticketId":"TKT-10001",
        "subject":"Unable to login",
        "status":"Resolved"
    }
]
```

---

# 3. Get Ticket by ID

### Endpoint

```
GET /tickets/{ticketId}
```

### Description

Retrieves detailed information for a specific ticket.

### Path Parameter

| Parameter | Description |
|------------|-------------|
| ticketId | Unique Ticket Identifier |

### Success Response

```json
{
    "ticketId":"TKT-10001",
    "subject":"Unable to login",
    "priority":"High",
    "category":"Authentication",
    "sentiment":"Negative",
    "status":"Resolved"
}
```

---

# 4. Update Ticket

### Endpoint

```
PUT /tickets/{ticketId}
```

### Description

Updates an existing support ticket.

### Path Parameter

| Parameter | Description |
|------------|-------------|
| ticketId | Ticket Identifier |

### Request Body

```json
{
    "subject":"Updated Subject",
    "description":"Updated Description"
}
```

### Success Response

```json
{
    "message":"Ticket Updated Successfully"
}
```

---

# 5. Delete Ticket

### Endpoint

```
DELETE /tickets/{ticketId}
```

### Description

Deletes an existing ticket.

### Path Parameter

| Parameter | Description |
|------------|-------------|
| ticketId | Ticket Identifier |

### Success Response

```json
{
    "message":"Ticket Deleted Successfully"
}
```

---

# 6. Get Approvals

### Endpoint

```
GET /approvals
```

### Description

Retrieves all approval requests pending or completed in the system.

### Success Response

```json
[
    {
        "approvalId":"APR-001",
        "status":"Pending"
    }
]
```

---

# 7. Get Orders

### Endpoint

```
GET /orders
```

### Description

Retrieves order information stored in the Orders table.

### Success Response

```json
[
    {
        "orderId":"ORD-101",
        "status":"Delivered"
    }
]
```

---

# 8. Approve Request

### Endpoint

```
GET /approve
```

### Description

Approves a pending action request.

The Approval Action Lambda validates the request and invokes the appropriate backend Lambda function (such as Issue Refund or Reset Password).

### Query Parameter

| Parameter | Description |
|------------|-------------|
| approvalId | Approval Request Identifier |

### Success Response

```json
{
    "message":"Request Approved"
}
```

---

# 9. Reject Request

### Endpoint

```
GET /reject
```

### Description

Rejects a pending approval request.

### Query Parameter

| Parameter | Description |
|------------|-------------|
| approvalId | Approval Request Identifier |

### Success Response

```json
{
    "message":"Request Rejected"
}
```

---


# Frontend Integration

The frontend application is developed using React with Vite and deployed using AWS Amplify Hosting.

Frontend responsibilities:

- User authentication using Amazon Cognito
- Sending authenticated API requests
- Ticket creation and management UI
- Displaying AI-generated ticket analysis
- Role-based UI rendering for CUSTOMER and SUPPORT users

Communication Flow:

React UI
   |
   |
Amazon Cognito Authentication
   |
   |
API Gateway REST APIs
   |
   |
AWS Lambda Backend

---

# Internal Backend APIs

The following backend components are **not exposed through API Gateway** and operate internally within the application.

| Component | Trigger |
|------------|---------|
| Processor Lambda | Amazon SQS |
| Bedrock Knowledge Base | Processor Lambda |
| Amazon Bedrock Agent | Processor Lambda / Agent Invocation|
| GetOrderStatus Lambda | Bedrock Agent |
| IssueRefund Lambda | Bedrock Agent |
| ResetPassword Lambda | Bedrock Agent |
| ApprovalRequest Lambda | Bedrock Agent |

---

# Error Responses

| Status Code | Description |
|-------------|-------------|
|200|Request Successful|
|400|Invalid Request|
|401|Unauthorized|
|404|Resource Not Found|
|500|Internal Server Error|

---

# API Workflow

1. User accesses the React application hosted on AWS Amplify.

2. User authenticates using Amazon Cognito.

3. React frontend receives authentication tokens from Cognito.

4. React application sends authenticated HTTP requests to Amazon API Gateway.

5. API Gateway validates Cognito JWT tokens.

6. API Gateway invokes the appropriate AWS Lambda function.

7. Lambda performs the requested business logic.

8. Ticket-related operations store data in Amazon DynamoDB.

9. Ticket creation events are published to Amazon SQS.

10. Processor Lambda consumes SQS messages and invokes Amazon Bedrock.

11. AI analysis updates ticket information in DynamoDB.

12. React frontend retrieves and displays updated ticket information through REST APIs.

---

# Summary

The AI Ticket Triage Assistant exposes RESTful APIs for ticket management, approvals, and order retrieval while leveraging asynchronous processing and Generative AI services internally. This architecture ensures responsive user interactions while enabling scalable AI-powered ticket processing.