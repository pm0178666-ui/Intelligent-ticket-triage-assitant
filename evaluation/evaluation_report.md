# Intelligent Customer Support Ticket Triage & Resolution Assistant

## Evaluation Report

---

### Dataset

- Total Tickets Evaluated : 50

- Ticket Types
  - Password Reset Enquiry
  - Password Reset
  - Order Status
  - Refund

---

## Processing Results

| Metric | Result |
|---------|--------|
| Tickets Processed | 50/50 |
| Success Rate | 100.0% |
| Draft Responses Generated | 50/50 (100.0%) |

---

## Classification Accuracy

| Metric | Accuracy |
|---------|----------|
| Category Accuracy | 98.0% |
| Priority Accuracy | 44.0% |
| Sentiment Accuracy | 58.0% |

---

## Performance

| Metric | Value |
|---------|-------|
| Average Processing Time | 4.57 sec |
| Fastest Ticket | 3.87 sec |
| Slowest Ticket | 7.58 sec |

---

## Evaluation Summary

The Ticket Triage Assistant successfully processed all evaluation tickets.

The AI generated draft responses for every ticket submitted.

Semantic category matching was used during evaluation because the LLM may return equivalent category names such as **Order Tracking**, **Order Inquiry**, or **Account Management** while still correctly identifying the user's intent.

Overall, the application demonstrates reliable end-to-end ticket ingestion, AI-powered classification, draft response generation, and backend processing using AWS serverless services and Amazon Bedrock.

