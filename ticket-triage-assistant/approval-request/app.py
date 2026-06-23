import json
import boto3
import uuid
import os

from decimal import Decimal
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

TABLE_NAME = os.environ["APPROVALS_TABLE"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

table = dynamodb.Table(TABLE_NAME)

TICKETS_TABLE = os.environ["TICKETS_TABLE"]
tickets_table = dynamodb.Table(TICKETS_TABLE)


def lambda_handler(event, context):

    print("EVENT:", event)

    function_name = event.get("function")

    approval_id = str(uuid.uuid4())

    # =========================
    # Refund Approval
    # =========================
    if function_name == "createRefundApproval":

        print("FUNCTION PARAMETERS:")
        print(event.get("parameters"))
        

        order_id = None
        amount = None

        for param in event.get("parameters", []):
            if param["name"] == "orderId":
                order_id = param["value"]

            elif param["name"] == "amount":
                amount = Decimal(str(param["value"]))

        action_type = "ISSUE_REFUND"


        ticket_id = event.get("sessionId")

        payload = {
            "ticketId": ticket_id,
            "orderId": order_id,
            "amount": amount
        }

        result_text = (
            f"Refund approval request created for order "
            f"{order_id}. Awaiting human approval."
        )

    # =========================
    # Password Reset Approval
    # =========================
    elif function_name == "createPasswordResetApproval":

        print("NEW PASSWORD RESET")
    
        ticket_id = event.get("sessionId")

        ticket_response = tickets_table.get_item(
            Key={
                "ticketId": ticket_id
            }
        )

        ticket = ticket_response.get("Item", {})

        print("Ticket Response:", ticket_response)

        customer_email = ticket.get("customerEmail")

        if not customer_email:
    
            result_text = (
                "Unable to create password reset approval. "
                "Customer email not found."
            )

            return {
                "messageVersion": "1.0",
                "response": {
                    "actionGroup": event["actionGroup"],
                    "function": event["function"],
                    "functionResponse": {
                        "responseBody": {
                            "TEXT": {
                                "body": result_text
                            }
                        }
                    }
                }
            }

        print("Customer Email:", customer_email)

        action_type = "PASSWORD_RESET"

        payload = {
            "ticketId": ticket_id,
            "customerEmail": customer_email
        }

        result_text = (
            f"Password reset approval request created for "
            f"{customer_email}. Awaiting human approval."
        )

        print("PAYLOAD SAVED:", payload)

    else:

        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event["actionGroup"],
                "function": event["function"],
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": "Unknown function."
                        }
                    }
                }
            }
        }

    # =========================
    # Save Approval Request
    # =========================

    print("PAYLOAD SAVED:", payload)
    table.put_item(
        Item={
            "approvalId": approval_id,
            "actionType": action_type,
            "payload": payload,
            "status": "PENDING",
            "createdAt": datetime.now(timezone.utc).isoformat()
        }
    )

    # =========================
    # Approval Links
    # =========================
    approve_link = (
        f"https://xesajug973.execute-api.us-east-1.amazonaws.com/Prod/approve"
        f"?approvalId={approval_id}&action=approve"
    )

    reject_link = (
        f"https://xesajug973.execute-api.us-east-1.amazonaws.com/Prod/reject"
        f"?approvalId={approval_id}&action=reject"
    )

    # =========================
    # SNS Notification
    # =========================
    message = f"""
APPROVAL REQUIRED

Action Type: {action_type}

Approval ID: {approval_id}

Approve:
{approve_link}

Reject:
{reject_link}
"""

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="Ticket Approval Required",
        Message=message
    )

    # =========================
    # Bedrock Response
    # =========================
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": event["actionGroup"],
            "function": event["function"],
            "functionResponse": {
                "responseBody": {
                    "TEXT": {
                        "body": result_text
                    }
                }
            }
        }
    }