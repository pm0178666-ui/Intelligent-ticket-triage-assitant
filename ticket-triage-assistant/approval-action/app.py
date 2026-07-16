import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["APPROVALS_TABLE"])

lambda_client = boto3.client("lambda")

# tool lambdas from environment (IMPORTANT)
ISSUE_REFUND_FN = os.environ["ISSUE_REFUND_FN"]
RESET_PASSWORD_FN = os.environ["RESET_PASSWORD_FN"]

def decimal_converter(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        },
        "body": json.dumps(body, default=decimal_converter)
    }


def lambda_handler(event, context):

    if event.get("httpMethod") == "OPTIONS":
        return response(200, {})

    print("EVENT:", event)

    params = event.get("queryStringParameters") or {}

    approval_id = params.get("approvalId")
    action = params.get("action")  # approve / reject

    if not approval_id or not action:
        return response(400, "Missing approvalId or action")

    # Fetch approval request
    db_response = table.get_item(Key={"approvalId": approval_id})
    item = response.get("Item")

    if not item:
        return response(404, "Approval not found")

    # Decide status
    new_status = "APPROVED" if action == "approve" else "REJECTED"

    # Update status in DB
    table.update_item(
        Key={"approvalId": approval_id},
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": new_status}
    )

    print("Approval Status Updated:", new_status)

    # If rejected → stop flow
    if new_status == "REJECTED":
        return response(200, {
            "message": "Request REJECTED",
            "approvalId": approval_id
    })

    # Approved → execute tool
    action_type = item.get("actionType")
    payload = item.get("payload", {})

    print("Executing tool:", action_type)
    print("Payload:", payload)


    try:
        if action_type == "ISSUE_REFUND":
            lambda_client.invoke(
                FunctionName=ISSUE_REFUND_FN,
                InvocationType="Event",
                Payload=json.dumps(payload, default=decimal_converter)
            )

        elif action_type == "PASSWORD_RESET":
            lambda_client.invoke(
                FunctionName=RESET_PASSWORD_FN,
                InvocationType="Event",
                Payload=json.dumps(payload, default=decimal_converter)
            )

        else:
            return response(400, "Unknown actionType")

    except Exception as e:
        print("Tool execution failed:", str(e))
        return response(500, "Tool execution failed")

    return response(200, {
        "message": "Approved and executed successfully",
        "approvalId": approval_id,
        "actionType": action_type
})