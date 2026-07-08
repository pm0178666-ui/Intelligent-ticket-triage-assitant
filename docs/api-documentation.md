# API Documentation

## Overview

The AI Ticket Triage Assistant exposes a RESTful API through Amazon API Gateway. These APIs enable ticket management, approval workflows, and order retrieval while backend AI processing is handled asynchronously using Amazon SQS and AWS Lambda.

---

# Base URL

```
https://xesajug973.execute-api.us-east-1.amazonaws.com/Prod
```

---

# Authentication

The application uses Amazon Cognito for user authentication.

Authenticated users receive a JWT token, which is used to access protected API endpoints through the frontend application.

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

# Internal Backend APIs

The following backend components are **not exposed through API Gateway** and operate internally within the application.

| Component | Trigger |
|------------|---------|
| Processor Lambda | Amazon SQS |
| Bedrock Knowledge Base | Processor Lambda |
| Amazon Bedrock Agent | Processor Lambda |
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

1. Client sends an HTTP request through the Streamlit application.
2. Amazon API Gateway receives the request.
3. API Gateway invokes the appropriate AWS Lambda function.
4. Lambda performs the requested business logic.
5. Ticket-related operations store data in Amazon DynamoDB.
6. Ticket creation events are published to Amazon SQS.
7. The Processor Lambda consumes the message and invokes Amazon Bedrock.
8. AI analysis updates the ticket information in DynamoDB.
9. The frontend retrieves updated ticket information using the REST APIs.

---

# Summary

The AI Ticket Triage Assistant exposes RESTful APIs for ticket management, approvals, and order retrieval while leveraging asynchronous processing and Generative AI services internally. This architecture ensures responsive user interactions while enabling scalable AI-powered ticket processing.