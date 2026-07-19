import csv
import time
import requests

# ============================================================
# CONFIGURATION
# ============================================================

CREATE_TICKET_API = "https://xesajug973.execute-api.us-east-1.amazonaws.com/Prod/tickets"
GET_TICKET_API = "https://xesajug973.execute-api.us-east-1.amazonaws.com/Prod/tickets/{}"

INPUT_CSV = "sample_tickets.csv"
OUTPUT_CSV = "evaluation_results.csv"

CUSTOMER_NAME = "Evaluation User"
CUSTOMER_EMAIL = "evaluation@example.com"

POLL_INTERVAL = 2
TIMEOUT = 60


# ============================================================
# CATEGORY MAPPING
# ============================================================

CATEGORY_MAPPING = {

    "Password Reset Enquiry": [
        "Account Management",
        "Account Access",
        "Account Help",
        "Account Recovery",
        "Password Support",
        "Technical Support"
    ],

    "Password Reset": [
        "Account Management",
        "Account Access",
        "Account Recovery",
        "Account Issues",
        "Access Request"
    ],

    "Order Status": [
        "Order Status",
        "Order Inquiry",
        "Order Tracking",
        "Order Update",
        "Package Tracking",
        "Delivery Inquiry",
        "Shipping"
    ],

    "Refund": [
        "Refund",
        "Refund Request",
        "Refunds",
        "Refund/Return"
    ]
}


# ============================================================
# HELPERS
# ============================================================

def normalize(text):
    return text.strip().lower()


def category_match(expected, actual):

    expected = expected.strip()

    actual = actual.strip()

    if normalize(expected) == normalize(actual):
        return True

    allowed = CATEGORY_MAPPING.get(expected, [])

    return any(normalize(actual) == normalize(item) for item in allowed)


def priority_match(expected, actual):
    return normalize(expected) == normalize(actual)


def sentiment_match(expected, actual):
    return normalize(expected) == normalize(actual)


# ============================================================
# CREATE TICKET
# ============================================================

def create_ticket(subject, message):

    payload = {
        "customerName": CUSTOMER_NAME,
        "customerEmail": CUSTOMER_EMAIL,
        "subject": subject,
        "message": message
    }

    response = requests.post(CREATE_TICKET_API, json=payload)

    response.raise_for_status()

    return response.json()["ticketId"]


# ============================================================
# GET TICKET
# ============================================================

def get_ticket(ticket_id):

    response = requests.get(GET_TICKET_API.format(ticket_id))

    response.raise_for_status()

    return response.json()


# ============================================================
# WAIT FOR PROCESSING
# ============================================================

def wait_until_processed(ticket_id):

    start = time.time()

    while True:

        ticket = get_ticket(ticket_id)

        status = ticket.get("status", "").lower()

        if status == "processed":

            latency = round(time.time() - start, 2)

            return ticket, latency

        if time.time() - start > TIMEOUT:

            return None, TIMEOUT

        time.sleep(POLL_INTERVAL)


# ============================================================
# MAIN
# ============================================================

def main():

    results = []

    with open(INPUT_CSV, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        rows = list(reader)

    total = len(rows)

    print("=" * 60)
    print(f"Evaluating {total} tickets")
    print("=" * 60)

    for i, row in enumerate(rows, start=1):

        print(f"\n[{i}/{total}] {row['subject']}")

        try:

            ticket_id = create_ticket(
                row["subject"],
                row["description"]
            )

            print("Ticket Created:", ticket_id)

            ticket, latency = wait_until_processed(ticket_id)

            if ticket is None:

                print("Timed Out")

                continue

            actual_category = ticket.get("category", "")
            actual_priority = ticket.get("priority", "")
            actual_sentiment = ticket.get("sentiment", "")

            category_ok = category_match(
                row["expected_category"],
                actual_category
            )

            priority_ok = priority_match(
                row["expected_priority"],
                actual_priority
            )

            sentiment_ok = sentiment_match(
                row["expected_sentiment"],
                actual_sentiment
            )

            results.append({

                "ticketId": ticket_id,

                "subject": row["subject"],

                "expected_category": row["expected_category"],
                "actual_category": actual_category,
                "category_match": category_ok,

                "expected_priority": row["expected_priority"],
                "actual_priority": actual_priority,
                "priority_match": priority_ok,

                "expected_sentiment": row["expected_sentiment"],
                "actual_sentiment": actual_sentiment,
                "sentiment_match": sentiment_ok,

                "processing_status": ticket.get("status"),

                "latency_seconds": latency,

                "draft_generated":
                    "Yes" if ticket.get("draftResponse") else "No"

            })

            print("Processed ✓")

        except Exception as e:

            print("ERROR:", e)

    if len(results) == 0:

        print("No results generated.")

        return

    with open(
        OUTPUT_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()

        writer.writerows(results)

    print("\nEvaluation Results Saved")

    category_accuracy = (
        sum(r["category_match"] for r in results)
        / len(results)
    ) * 100

    priority_accuracy = (
        sum(r["priority_match"] for r in results)
        / len(results)
    ) * 100

    sentiment_accuracy = (
        sum(r["sentiment_match"] for r in results)
        / len(results)
    ) * 100

    avg_latency = sum(
        r["latency_seconds"] for r in results
    ) / len(results)

    print("\n==================== SUMMARY ====================")

    print(f"Tickets Tested        : {len(results)}")
    print(f"Category Accuracy     : {category_accuracy:.2f}%")
    print(f"Priority Accuracy     : {priority_accuracy:.2f}%")
    print(f"Sentiment Accuracy    : {sentiment_accuracy:.2f}%")
    print(f"Average Latency       : {avg_latency:.2f} sec")

    print("=================================================")


if __name__ == "__main__":
    main()