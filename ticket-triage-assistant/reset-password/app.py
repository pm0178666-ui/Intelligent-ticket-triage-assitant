import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb")

ses = boto3.client(
    "ses",
    region_name="us-east-1"
)

tickets_table = dynamodb.Table(
    os.environ["TABLE_NAME"]
)

def lambda_handler(event, context):

    print("Received event:", event)

    ticket_id = event.get("ticketId")

    print("ticket_id =", ticket_id)


    if not ticket_id:
        return {
            "statusCode":400,
            "body":json.dumps({
                "error":"ticketId is required"
            })
        }

    ticket_response = tickets_table.get_item(
        Key={
            "ticketId": ticket_id
        }
    )

    ticket = ticket_response.get(
        "Item",
        {}
    )

    customer_email = ticket.get(
        "customerEmail"
    )

    print("customer_email =", customer_email)
    

    if not customer_email:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "customerEmail is required"
            })
        }
    
    # Generate dummy password reset link
    reset_token = str(uuid.uuid4())

    reset_link = (
        "https://ticket-support-demo.com/reset-password?"
        f"token={reset_token}"
    )

    print("Reset Link:", reset_link)

    # Send email using SES
    ses.send_email(

        Source="padmaja0925@gmail.com",

        Destination={
            "ToAddresses": [
                customer_email
            ]
        },

        Message={

            "Subject": {
                "Data": "Password Reset Link"
            },

            "Body": {

                "Text": {
                    "Data": f"""
Hello,

You requested a password reset.

Please use this link to reset your password:

{reset_link}

If you did not request this action, please contact support.

Regards,
Customer Support Team
"""
                }
            }
        }
    )

    print("Password reset email sent")
    
    response = {
        "status": "SUCCESS",
        "action": "PASSWORD_RESET",
        "customerEmail": customer_email,
        "message": f"Password reset link has been sent to {customer_email}"
    }


    print("Response:", response)

    if ticket_id:

        tickets_table.update_item(
            Key={
                "ticketId": ticket_id
            },
            UpdateExpression="""
                SET #s = :status,
                    draftResponse = :msg,
                    agentResponse = :msg,
                    resetLink = :link,
                    updatedAt = :updatedAt
            """,
            ExpressionAttributeNames={
                "#s": "status"
            },
            ExpressionAttributeValues={
                ":status": "PASSWORD_RESET_COMPLETED",
                ":msg": f"Password reset link has been sent to {customer_email}",
                ":link": reset_link,
                ":updatedAt": datetime.now().isoformat()
            }
        )

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }