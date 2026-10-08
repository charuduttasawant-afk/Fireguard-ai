import json
from datetime import datetime


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_transaction(transactions, transaction_id):
    for transaction in transactions:
        if transaction["transaction_id"] == transaction_id:
            return transaction
    return None


def find_customer(customers, customer_id):
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer
    return None


def analyze_customer_behavior(
    transaction_id,
    transaction_file="data/transactions.json",
    customer_file="data/customers.json"
):

    transactions = load_json(transaction_file)
    customers = load_json(customer_file)

    transaction = find_transaction(
        transactions,
        transaction_id
    )

    if not transaction:
        return {
            "agent": "Customer Behaviour Agent",
            "status": "EXCEPTION",
            "transaction_id": transaction_id,
            "message": "Transaction not found"
        }

    customer = find_customer(
        customers,
        transaction["customer_id"]
    )

    if not customer:
        return {
            "agent": "Customer Behaviour Agent",
            "status": "EXCEPTION",
            "transaction_id": transaction_id,
            "message": "Customer information unavailable"
        }

    findings = []

    # --------------------------------------------------
    # 1. LOCATION ANALYSIS
    # --------------------------------------------------

    transaction_location = transaction["location"]
    usual_location = customer["usual_location"]
    travel_history = customer.get("travel_history", [])

    if transaction_location == usual_location:

        findings.append({
            "signal": "Usual Location",
            "severity": "LOW",
            "description":
                f"Transaction occurred in the customer's "
                f"usual location: {usual_location}."
        })

    elif transaction_location in travel_history:

        findings.append({
            "signal": "Travel-Related Location",
            "severity": "MEDIUM",
            "description":
                f"Transaction occurred in {transaction_location}, "
                f"which differs from the usual location "
                f"({usual_location}) but appears in travel history."
        })

    else:

        findings.append({
            "signal": "Unusual Location",
            "severity": "HIGH",
            "description":
                f"Transaction occurred in {transaction_location}, "
                f"which differs from the usual location "
                f"({usual_location}) and is not present "
                f"in travel history."
        })

    # --------------------------------------------------
    # 2. TRANSACTION AMOUNT ANALYSIS
    # --------------------------------------------------

    transaction_amount = transaction["amount"]
    average_amount = customer["average_transaction"]

    ratio = transaction_amount / average_amount

    if ratio <= 2:

        findings.append({
            "signal": "Normal Transaction Amount",
            "severity": "LOW",
            "description":
                f"Transaction amount ₹{transaction_amount:,} "
                f"is within the customer's normal range "
                f"compared with the average of "
                f"₹{average_amount:,}."
        })

    elif ratio <= 3:

        findings.append({
            "signal": "Elevated Transaction Amount",
            "severity": "MEDIUM",
            "description":
                f"Transaction amount ₹{transaction_amount:,} "
                f"is higher than the customer's average "
                f"of ₹{average_amount:,}."
        })

    else:

        findings.append({
            "signal": "Highly Unusual Transaction Amount",
            "severity": "HIGH",
            "description":
                f"Transaction amount ₹{transaction_amount:,} "
                f"is more than three times the customer's "
                f"average of ₹{average_amount:,}."
        })

    # --------------------------------------------------
    # 3. TIME ANALYSIS
    # --------------------------------------------------

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

    if start_time <= transaction_time <= end_time:

        findings.append({
            "signal": "Normal Transaction Time",
            "severity": "LOW",
            "description":
                f"Transaction occurred at "
                f"{transaction_time.strftime('%H:%M')}, "
                f"within the customer's typical transaction hours."
        })

    else:

        findings.append({
            "signal": "Unusual Transaction Time",
            "severity": "HIGH",
            "description":
                f"Transaction occurred at "
                f"{transaction_time.strftime('%H:%M')}, "
                f"outside the customer's typical transaction hours."
        })

    # --------------------------------------------------
    # 4. CHANNEL ANALYSIS
    # --------------------------------------------------

    if transaction["channel"] == customer["usual_channel"]:

        findings.append({
            "signal": "Usual Channel",
            "severity": "LOW",
            "description":
                f"Transaction used the customer's usual channel: "
                f"{customer['usual_channel']}."
        })

    else:

        findings.append({
            "signal": "Unusual Channel",
            "severity": "MEDIUM",
            "description":
                f"Transaction used {transaction['channel']} "
                f"instead of the customer's usual channel "
                f"{customer['usual_channel']}."
        })

    # --------------------------------------------------
    # 5. BEHAVIOURAL ASSESSMENT
    # --------------------------------------------------

    high_count = sum(
        1 for finding in findings
        if finding["severity"] == "HIGH"
    )

    medium_count = sum(
        1 for finding in findings
        if finding["severity"] == "MEDIUM"
    )

    if high_count >= 2:
        assessment = "HIGH"

    elif high_count == 1 or medium_count >= 2:
        assessment = "MEDIUM"

    else:
        assessment = "LOW"

    return {
        "agent": "Customer Behaviour Agent",
        "status": "SUCCESS",
        "transaction_id": transaction["transaction_id"],
        "customer_id": transaction["customer_id"],
        "assessment": assessment,
        "customer_profile": {
            "usual_location": customer["usual_location"],
            "average_transaction": customer["average_transaction"],
            "usual_channel": customer["usual_channel"],
            "usual_device": customer["usual_device"],
            "travel_history": customer.get("travel_history", [])
        },
        "findings": findings
    }


# ------------------------------------------------------
# TEST THE AGENT
# ------------------------------------------------------

if __name__ == "__main__":

    test_cases = [
        "TXN1001",
        "TXN1002",
        "TXN1003"
    ]

    for transaction_id in test_cases:

        print("\n" + "=" * 60)

        result = analyze_customer_behavior(transaction_id)

        print(
            f"Transaction: {transaction_id}"
        )

        print(
            f"Customer Behaviour Assessment: "
            f"{result.get('assessment', 'N/A')}"
        )

        print("\nFindings:")

        for finding in result.get("findings", []):

            print(
                f"- {finding['signal']} "
                f"[{finding['severity']}]"
            )