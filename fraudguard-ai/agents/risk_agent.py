import json
from datetime import datetime


# ---------------------------------------------------------
# Load JSON data
# ---------------------------------------------------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


transactions = load_json("data/transactions.json")
customers = load_json("data/customers.json")
devices = load_json("data/devices.json")
rules = load_json("data/fraud_rules.json")


# ---------------------------------------------------------
# Find records
# ---------------------------------------------------------

def find_transaction(transaction_id):
    for transaction in transactions:
        if transaction["transaction_id"] == transaction_id:
            return transaction

    return None


def find_customer(customer_id):
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer

    return None


def find_device(device_id):
    for device in devices:
        if device["device_id"] == device_id:

            return device

    return None


# ---------------------------------------------------------
# Risk analysis
# ---------------------------------------------------------

def analyze_transaction(transaction_id):

    transaction = find_transaction(transaction_id)

    if not transaction:
        return {
            "status": "ERROR",
            "message": "Transaction not found"
        }

    customer = find_customer(transaction["customer_id"])
    device = find_device(transaction["device_id"])

    if not customer:
        return {
            "status": "EXCEPTION",
            "message": "Customer information unavailable"
        }

    if not device:
        return {
            "status": "EXCEPTION",
            "message": "Device information unavailable"
        }

    risk_score = 0
    findings = []

    # -----------------------------------------------------
    # Rule 1: New Device
    # -----------------------------------------------------

    if not device["known_device"]:

        risk_score += 20

        findings.append({
            "rule": "R001",
            "signal": "New Device",
            "risk_points": 20,
            "description": "Transaction originated from a device not previously associated with the customer."
        })


    # -----------------------------------------------------
    # Rule 2: Location
    # -----------------------------------------------------

    location = transaction["location"]

    if location != customer["usual_location"]:

        # Check whether customer has travelled there previously
        if location in customer.get("travel_history", []):

            findings.append({
                "rule": "R002",
                "signal": "Travel-related Location Difference",
                "risk_points": 0,
                "description": "Location differs from usual location but appears in customer travel history."
            })

        else:

            risk_score += 15

            findings.append({
                "rule": "R002",
                "signal": "Unusual Location",
                "risk_points": 15,
                "description": "Transaction location differs from usual customer location."
            })


    # -----------------------------------------------------
    # Rule 3: Transaction Amount
    # -----------------------------------------------------

    average_amount = customer["average_transaction"]
    transaction_amount = transaction["amount"]

    if transaction_amount > average_amount * 3:

        risk_score += 20

        findings.append({
            "rule": "R003",
            "signal": "Unusual Transaction Amount",
            "risk_points": 20,
            "description": (
                f"Transaction amount ₹{transaction_amount:,} "
                f"is significantly above customer average of "
                f"₹{average_amount:,}."
            )
        })


    # -----------------------------------------------------
    # Rule 4: Transaction Time
    # -----------------------------------------------------

    transaction_time = datetime.strptime(
        transaction["timestamp"],
        "%Y-%m-%d %H:%M"
    ).time()

    start_time = datetime.strptime(
        customer["typical_transaction_start"],
        "%H:%M"
    ).time()

    end_time = datetime.strptime(
        customer["typical_transaction_end"],
        "%H:%M"
    ).time()


    if not (start_time <= transaction_time <= end_time):

        risk_score += 10

        findings.append({
            "rule": "R004",
            "signal": "Unusual Transaction Time",
            "risk_points": 10,
            "description": "Transaction occurred outside the customer's typical transaction hours."
        })


    # -----------------------------------------------------
    # Rule 5: Unknown Merchant
    # -----------------------------------------------------

    if transaction["merchant"] == "Unknown Merchant":

        risk_score += 15

        findings.append({
            "rule": "R005",
            "signal": "Unknown Merchant",
            "risk_points": 15,
            "description": "Merchant is not identified in the available transaction context."
        })


    # -----------------------------------------------------
    # Determine risk level
    # -----------------------------------------------------

    if risk_score >= 60:
        risk_level = "HIGH"

    elif risk_score >= 30:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"


    # -----------------------------------------------------
    # Determine HITL and escalation
    # -----------------------------------------------------

    human_review_required = risk_level in ["MEDIUM", "HIGH"]

    escalation_required = risk_level == "HIGH"


    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------

    return {
        "status": "SUCCESS",
        "transaction_id": transaction["transaction_id"],
        "customer_id": transaction["customer_id"],
        "risk_score": risk_score,
        "risk_level": risk_level,
        "human_review_required": human_review_required,
        "escalation_required": escalation_required,
        "findings": findings
    }


# ---------------------------------------------------------
# Test the three mandatory cases
# ---------------------------------------------------------

if __name__ == "__main__":

    test_transactions = [
        "TXN1001",
        "TXN1002",
        "TXN1003"
    ]

    print("\n========================================")
    print("      FRAUDGUARD AI - RISK ENGINE")
    print("========================================\n")

    for transaction_id in test_transactions:

        result = analyze_transaction(transaction_id)

        print("----------------------------------------")
        print(f"Transaction : {transaction_id}")

        if result["status"] != "SUCCESS":
            print(f"Status      : {result['status']}")
            print(f"Message     : {result['message']}")
            continue

        print(f"Risk Score  : {result['risk_score']}")
        print(f"Risk Level  : {result['risk_level']}")
        print(f"HITL        : {result['human_review_required']}")
        print(f"Escalation  : {result['escalation_required']}")

        print("\nFindings:")

        if result["findings"]:

            for finding in result["findings"]:

                print(
                    f"  - {finding['signal']} "
                    f"(+{finding['risk_points']})"
                )

        else:

            print("  - No significant anomalies detected")

        print()