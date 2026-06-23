import json
import boto3
import os
from datetime import datetime

# =========================
# ENV VARIABLES
# =========================
AGENT_ID = os.environ["AGENT_ID"]
AGENT_ALIAS_ID = os.environ["AGENT_ALIAS_ID"]
REGION = os.environ.get("AWS_REGION", "us-east-1")
TABLE_NAME = os.environ["TABLE_NAME"]

# =========================
# CLIENTS
# =========================
bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION)
bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)

table = dynamodb.Table(TABLE_NAME)

# =========================
# 1. CLASSIFICATION STEP
# =========================
def classify_ticket(subject, message):

    classification_prompt = f"""
    You are a strict ticket classifier.

    Return ONLY valid JSON with no explanation:

    {{
        "category": "",
        "priority": "",
        "sentiment": ""
    }}

    Subject: {subject}
    Message: {message}
    """

    response = bedrock_runtime.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[
            {
                "role": "user",
                "content": [
                    {"text": classification_prompt}
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 200,
            "temperature": 0
        }
    )

    text = response["output"]["message"]["content"][0]["text"]

    # Clean response
    text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end+1]

    return json.loads(text)


# =========================
# 2. AGENT CALL STEP
# =========================
def call_agent(ticket_id, subject, message):

    input_text = f"""
    TicketId: {ticket_id}
    Subject: {subject}
    Message: {message}
    """


    print("========== AGENT INPUT ==========")
    print(input_text)

    print("Using Agent:", AGENT_ID)
    print("Using Alias:", AGENT_ALIAS_ID)

    response = bedrock_agent_runtime.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=ticket_id,
        inputText=input_text,
        sessionState={
            "sessionAttributes": {
                "ticketId": ticket_id
            }
        }
    )

    print("Agent Session ID:", response["sessionId"])

    print("========== FULL AGENT RESPONSE ==========")
    print(response)

    output = ""

    for event in response["completion"]:

        print("FULL EVENT =>")
        print(event)

        if "chunk" in event:
            text = event["chunk"]["bytes"].decode("utf-8")

            print("CHUNK =>")
            print(text)

            output += text

        if "trace" in event:
            print("TRACE =>")
            print(json.dumps(event["trace"], indent=2, default=str))

    return output


# =========================
# 3. LAMBDA HANDLER
# =========================
def lambda_handler(event, context):

    print("Processor Lambda Triggered")

    for record in event["Records"]:

        body = json.loads(record["body"])

        ticket_id = body["ticketId"]
        subject = body.get("subject", "")
        message = body.get("message", "")

        print(f"Processing Ticket: {ticket_id}")

        # =========================
        # STEP 1: CLASSIFICATION
        # =========================
        classification = classify_ticket(subject, message)

        category = classification.get("category", "unknown")
        priority = classification.get("priority", "low")
        sentiment = classification.get("sentiment", "neutral")

        print("Classification Done:", classification)

        # =========================
        # STEP 2: AGENT PROCESSING
        # =========================
        agent_response = call_agent(ticket_id, subject, message)

        print("Agent Response:", agent_response)

        # =========================
        # STEP 3: STORE IN DYNAMODB
        # =========================
        table.update_item(
            Key={"ticketId": ticket_id},
            UpdateExpression="""
                SET category = :c,
                    priority = :p,
                    sentiment = :s,
                    draftResponse = :r,
                    #st = :status,
                    updatedAt = :t
            """,
            ExpressionAttributeNames={
                "#st": "status"
            },
            ExpressionAttributeValues={
                ":c": category,
                ":p": priority,
                ":s": sentiment,
                ":r": agent_response,
                ":status": "processed",
                ":t": datetime.utcnow().isoformat()
            }
        )

        print("DynamoDB updated successfully")

    return {
        "statusCode": 200,
        "body": json.dumps("Processor completed successfully")
    }