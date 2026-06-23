import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):

    print("EVENT:", event)

    order_id = None

    for param in event.get("parameters", []):
        if param["name"] == "orderId":
            order_id = param["value"]

    if not order_id:

        result_text = "orderId is required"

    else:

        response = table.get_item(
            Key={
                "orderId": order_id
            }
        )

        item = response.get("Item")

        if not item:

            result_text = f"Order {order_id} not found"

        else:

            result_text = (
                f"Order {order_id} belongs to "
                f"{item['customerName']}. "
                f"Current status is {item['status']}. "
                f"Amount is {item['amount']}."
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