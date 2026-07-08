import requests

BASE_URL = "https://xesajug973.execute-api.us-east-1.amazonaws.com/Prod"




#pOST TICKET(Creating ticket)
def create_ticket(payload):

    try:

        response = requests.post(
            f"{BASE_URL}/tickets",
            json=payload
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        raise Exception(
            f"Failed to create ticket: {e}"
        )
    


#GET TICKETS(Fetching tickets)
def get_tickets():
    
    response = requests.get(
        f"{BASE_URL}/tickets"
    )

    response.raise_for_status()

    return response.json()


# GET TICKET BY ID(Each ticket)
def get_ticket_by_id(ticket_id):

    response = requests.get(
        f"{BASE_URL}/tickets/{ticket_id}"
    )

    response.raise_for_status()

    return response.json()

# 
def get_approvals():
    
    response = requests.get(
        f"{BASE_URL}/approvals"
    )

    response.raise_for_status()

    return response.json()

#
def approve_request(approval_id):
    
    response = requests.get(
        f"{BASE_URL}/approve",
        params={
            "approvalId": approval_id,
            "action": "approve"
        }
    )
    response.raise_for_status()

    return response.json()


def reject_request(approval_id):
    
    response = requests.get(
        f"{BASE_URL}/reject",
        params={
            "approvalId": approval_id,
            "action": "reject"
        }
    )

    response.raise_for_status()

    return response.json()


# GET ORDERS
def get_orders():

    response = requests.get(
        f"{BASE_URL}/orders"
    )

    response.raise_for_status()

    return response.json()