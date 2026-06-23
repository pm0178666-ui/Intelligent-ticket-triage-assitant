import boto3
import json
import os
from datetime import datetime

dynamodb = boto3.resource("dynamodb")

tickets_table = dynamodb.Table(
    os.environ["TABLE_NAME"]
)

def lambda_handler(event, context):

    print("Received event:", event)

    ticket_id = event.get("ticketId")
    order_id = event.get("orderId")
    amount = event.get("amount")

    if not ticket_id:
        return {
        "statusCode": 400,
        "body": json.dumps({
            "error": "ticketId is required"
        })
    }

    if not order_id or amount is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "orderId and amount are required"
            })
        }

    refund_reference = f"REF-{order_id}"

    response = {
        "status": "SUCCESS",
        "action": "REFUND_ISSUED",
        "orderId": order_id,
        "amount": amount,
        "refundReference": refund_reference,
        "message": "Refund has been successfully processed."
    }

    print("Response:", response)


    tickets_table.update_item(
        Key={
            "ticketId": ticket_id
        },
        UpdateExpression="""
            SET #s = :status,
                draftResponse = :msg,
                agentResponse = :msg,
                updatedAt = :updatedAt
        """,
        ExpressionAttributeNames={
            "#s": "status"
        },
        ExpressionAttributeValues={
            ":status": "REFUND_ISSUED",
            ":msg": "Refund has been successfully processed.",
            ":updatedAt": datetime.utcnow().isoformat()
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }