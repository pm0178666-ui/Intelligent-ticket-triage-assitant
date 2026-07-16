import json
import uuid
import boto3
import os
import logging
import traceback
from datetime import datetime

# AWS Clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
sqs = boto3.client("sqs")

# Environment variables
TABLE_NAME = os.environ["TABLE_NAME"]
QUEUE_URL = os.environ["QUEUE_URL"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
approvals_table = dynamodb.Table(
    os.environ["APPROVALS_TABLE"]
)
orders_table = dynamodb.Table(
    os.environ["ORDERS_TABLE"]
)

PRESIGNED_EXPIRY = int(os.environ.get("PRESIGNED_EXPIRY", "3600"))

# DynamoDB table resource
table = dynamodb.Table(TABLE_NAME)

# Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def iso_now():
    return datetime.utcnow().isoformat() + "Z"

def make_attachment_key(ticket_id: str, filename: str) -> str:
    ts = int(datetime.utcnow().timestamp() * 1000)
    safe_filename = filename.replace(" ", "_")
    return f"{ticket_id}/{ts}-{safe_filename}"

def lambda_handler(event, context):
    
    try:

        logger.info(
            "Received event: %s",
            json.dumps(event)
        )


        http_method = event.get(
            "httpMethod"
        )

        # Handle CORS preflight request
        if http_method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
                },
                "body": ""
            }

        path = event.get(
            "resource",
            ""
        )

        path_params = event.get(
            "pathParameters",
            {}
        )

        ticket_id = None

        if path_params:
            ticket_id = path_params.get(
                "ticketId"
            )



        # ==========================
        # GET SINGLE TICKET
        # ==========================
        if http_method == "GET" and ticket_id:

            response = table.get_item(
                Key={
                    "ticketId": ticket_id
                }
            )

            item = response.get(
                "Item"
            )

            if not item:

                return {
                    "statusCode": 404,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps({
                        "message": "Ticket not found"
                    })
                }

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(
                    item,
                    default=str
                )
            }
        

        # ==========================
        # GET ALL APPROVALS
        # ==========================

        if http_method == "GET" and path == "/approvals":

            response = approvals_table.scan()

            approvals = response.get(
                "Items",
                []
            )

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(
                    approvals,
                    default=str
                )
            }
        

        # ==========================
        # GET ALL ORDERS
        # ==========================

        if http_method == "GET" and path == "/orders":

            response = orders_table.scan()

            orders = response.get(
                "Items",
                []
            )

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(
                    orders,
                    default=str
                )
            }


        # ==========================
        # GET ALL TICKETS
        # ==========================
        if http_method == "GET":

            response = table.scan()

            tickets = response.get(
                "Items",
                []
            )

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(
                    tickets,
                    default=str
                )
            }
        

        # ==========================
        # UPDATE TICKET
        # ==========================
        if http_method == "PUT" and ticket_id:

            body = json.loads(
                event.get(
                    "body",
                    "{}"
                )
            )

            table.update_item(

                Key={
                    "ticketId": ticket_id
                },

                UpdateExpression="""
                    SET subject = :subject,
                        message = :message,
                        updatedAt = :updatedAt
                """,

                ExpressionAttributeValues={
                    ":subject": body.get("subject"),
                    ":message": body.get("message"),
                    ":updatedAt": iso_now()
                }
            )

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "message": "Ticket updated successfully"
                })
            }
        

        # ==========================
        # DELETE TICKET
        # ==========================
        if http_method == "DELETE" and ticket_id:

            table.delete_item(
                Key={
                    "ticketId": ticket_id
                }
            )


            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "message": "Ticket deleted successfully"
                })
            }          


        # ==========================
        # CREATE TICKET
        # ==========================

        body = json.loads(
            event.get(
                "body",
                "{}"
            )
        )

        # Generate ticket id and timestamp
        ticket_id = str(uuid.uuid4())
        created_at = iso_now()

        # Attachment handling
        filename = body.get("filename")
        attachment_key = None
        upload_url = None

        #Generating pre-signed URL
        if filename:
            attachment_key = make_attachment_key(ticket_id, filename)
            upload_url = s3.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": BUCKET_NAME,
                    "Key": attachment_key,
                    "ContentType": body.get("contentType", "image/png")
                },
                ExpiresIn=PRESIGNED_EXPIRY
            )

        # Build DynamoDB item
        item = {
            "ticketId": ticket_id,
            "customerName": body.get("customerName"),
            "customerEmail": body.get("customerEmail"),
            "subject": body.get("subject"),
            "message": body.get("message"),
            "source": body.get("source", "WEB"),
            "status": "OPEN",
            "category": "PENDING",
            "priority": "PENDING",
            "complexity": "PENDING",
            "attachmentKey": attachment_key,
            "createdAt": created_at
        }
        item = {k: v for k, v in item.items() if v is not None}

        # Persist to DynamoDB
        table.put_item(Item=item)
        logger.info("Stored ticket in DynamoDB: %s", ticket_id)

        # Send richer payload to SQS
        sqs_payload = {
            "ticketId": ticket_id,
            "customerName": item.get("customerName"),
            "customerEmail": item.get("customerEmail"),
            "subject": item.get("subject"),
            "message": item.get("message"),
            "attachmentKey": item.get("attachmentKey"),
            "createdAt": created_at
        }
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(sqs_payload))
        logger.info("Sent message to SQS: %s", ticket_id)

        # Build response
        response_body = {"ticketId": ticket_id, "status": "OPEN"}
        if upload_url:
            response_body["uploadUrl"] = upload_url

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response_body)
        }

    except Exception as e:
        logger.error("Unhandled exception: %s", str(e))
        logger.error(traceback.format_exc())
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }
