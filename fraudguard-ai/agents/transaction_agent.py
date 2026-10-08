import json
from datetime import datetime


def load_transactions(
    path="data/transactions.json"
):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_transaction(
    transactions,
    transaction_id
):
    for transaction in transactions:

        if transaction["transaction_id"] == transaction_id:
            return transaction

    return None


def analyze_transaction(
    transaction_id,
    transaction_file="data/transactions.json"
):

    transactions = load_transactions(
        transaction_file
    )

    transaction = find_transaction(
        transactions,
        transaction_id
    )

    # -----------------------------------------
    # Transaction not found
    # -----------------------------------------

    if not transaction:

        return {
            "agent": "Transaction Analysis Agent",
            "status": "EXCEPTION",
            "transaction_id": transaction_id,
            "message": "Transaction not found"
        }

    findings = []

    # -----------------------------------------
    # Transaction amount
    # -----------------------------------------

    amount = transaction["amount"]

    if amount >= 100000:

        findings.append({
            "signal": "Very High Transaction Amount",
            "severity": "HIGH",
            "description":
                f"Transaction amount is ₹{amount:,}."
        })

    elif amount >= 30000:

        findings.append({
            "signal": "Elevated Transaction Amount",
            "severity": "MEDIUM",
            "description":
                f"Transaction amount is ₹{amount:,}."
        })

    # -----------------------------------------
    # Transaction time
    # -----------------------------------------

    timestamp = datetime.strptime(
        transaction["timestamp"],
        "%Y-%m-%d %H:%M"
    )

    hour = timestamp.hour

    if hour < 6 or hour >= 23:

        findings.append({
            "signal": "Unusual Transaction Time",
            "severity": "MEDIUM",
            "description":
                f"Transaction occurred at {timestamp.strftime('%H:%M')}."
        })

    # -----------------------------------------
    # Merchant
    # -----------------------------------------

    if transaction["merchant"] == "Unknown Merchant":

        findings.append({
            "signal": "Unknown Merchant",
            "severity": "HIGH",
            "description":
                "Merchant identity is unavailable or unknown."
        })

    # -----------------------------------------
    # Location
    # -----------------------------------------

    if transaction["location"]:

        findings.append({
            "signal": "Transaction Location",
            "severity": "INFO",
            "description":
                f"Transaction originated from "
                f"{transaction['location']}."
        })

    # -----------------------------------------
    # Channel
    # -----------------------------------------

    findings.append({
        "signal": "Transaction Channel",
        "severity": "INFO",
        "description":
            f"Transaction was performed through "
            f"{transaction['channel']}."
    })

    # -----------------------------------------
    # Determine transaction-level assessment
    # -----------------------------------------

    high_count = sum(
        1 for finding in findings
        if finding["severity"] == "HIGH"
    )

    medium_count = sum(
        1 for finding in findings
        if finding["severity"] == "MEDIUM"
    )

    if high_count >= 1:

        assessment = "HIGH"

    elif medium_count >= 1:

        assessment = "MEDIUM"

    else:

        assessment = "LOW"

    # -----------------------------------------
    # Return structured result
    # -----------------------------------------

    return {

        "agent": "Transaction Analysis Agent",

        "status": "SUCCESS",

        "transaction_id":
            transaction["transaction_id"],

        "assessment":
            assessment,

        "transaction": {
            "amount": transaction["amount"],
            "timestamp": transaction["timestamp"],
            "merchant": transaction["merchant"],
            "location": transaction["location"],
            "channel": transaction["channel"],
            "device_id": transaction["device_id"]
        },

        "findings": findings
    }


# ---------------------------------------------
# Local testing
# ---------------------------------------------

if __name__ == "__main__":

    test_cases = [
        "TXN1001",
        "TXN1002",
        "TXN1003"
    ]

    for transaction_id in test_cases:

        print("\n" + "=" * 50)

        result = analyze_transaction(
            transaction_id
        )

        print(
            f"Transaction: {transaction_id}"
        )

        print(
            f"Assessment: "
            f"{result.get('assessment', 'N/A')}"
        )

        print("\nFindings:")

        for finding in result.get(
            "findings",
            []
        ):

            print(
                f"- {finding['signal']} "
                f"[{finding['severity']}]"
            )