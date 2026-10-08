import json


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


def find_device(devices, device_id):
    for device in devices:
        if device["device_id"] == device_id:
            return device
    return None


def analyze_device_behavior(
    transaction_id,
    transaction_file="data/transactions.json",
    customer_file="data/customers.json",
    device_file="data/devices.json"
):

    transactions = load_json(transaction_file)
    customers = load_json(customer_file)
    devices = load_json(device_file)

    transaction = find_transaction(
        transactions,
        transaction_id
    )

    if not transaction:
        return {
            "agent": "Device/Channel Agent",
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
            "agent": "Device/Channel Agent",
            "status": "EXCEPTION",
            "transaction_id": transaction_id,
            "message": "Customer information unavailable"
        }

    device = find_device(
        devices,
        transaction["device_id"]
    )

    if not device:
        return {
            "agent": "Device/Channel Agent",
            "status": "EXCEPTION",
            "transaction_id": transaction_id,
            "message": "Device information unavailable"
        }

    findings = []

    # --------------------------------------------------
    # 1. DEVICE ANALYSIS
    # --------------------------------------------------

    if device["known_device"]:

        findings.append({
            "signal": "Known Device",
            "severity": "LOW",
            "description":
                "Transaction originated from a device "
                "previously associated with the customer."
        })

    else:

        findings.append({
            "signal": "New Device",
            "severity": "HIGH",
            "description":
                "Transaction originated from a device "
                "not previously associated with the customer."
        })

    # --------------------------------------------------
    # 2. DEVICE OWNERSHIP ANALYSIS
    # --------------------------------------------------

    if device["customer_id"] == transaction["customer_id"]:

        findings.append({
            "signal": "Device-Customer Match",
            "severity": "LOW",
            "description":
                "The device is associated with the "
                "transaction customer."
        })

    else:

        findings.append({
            "signal": "Device-Customer Mismatch",
            "severity": "HIGH",
            "description":
                "The device is associated with a different "
                "customer."
        })

    # --------------------------------------------------
    # 3. CHANNEL ANALYSIS
    # --------------------------------------------------

    transaction_channel = transaction["channel"]
    usual_channel = customer["usual_channel"]

    if transaction_channel == usual_channel:

        findings.append({
            "signal": "Usual Banking Channel",
            "severity": "LOW",
            "description":
                f"Transaction used the customer's usual "
                f"channel: {usual_channel}."
        })

    else:

        findings.append({
            "signal": "Unusual Banking Channel",
            "severity": "MEDIUM",
            "description":
                f"Transaction used {transaction_channel} "
                f"instead of the customer's usual channel "
                f"{usual_channel}."
        })

    # --------------------------------------------------
    # 4. DEVICE + CHANNEL COMBINATION
    # --------------------------------------------------

    if (
        not device["known_device"]
        and transaction_channel != usual_channel
    ):

        findings.append({
            "signal": "New Device + Unusual Channel",
            "severity": "HIGH",
            "description":
                "Transaction combines a new device with "
                "a banking channel different from the "
                "customer's usual channel."
        })

    # --------------------------------------------------
    # 5. OVERALL DEVICE ASSESSMENT
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

    elif high_count == 1 or medium_count >= 1:
        assessment = "MEDIUM"

    else:
        assessment = "LOW"

    return {
        "agent": "Device/Channel Agent",
        "status": "SUCCESS",
        "transaction_id": transaction["transaction_id"],
        "customer_id": transaction["customer_id"],
        "assessment": assessment,
        "device_profile": {
            "device_id": transaction["device_id"],
            "known_device": device["known_device"],
            "device_customer_id": device["customer_id"],
            "transaction_channel": transaction_channel,
            "usual_channel": usual_channel
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

        result = analyze_device_behavior(transaction_id)

        print(
            f"Transaction: {transaction_id}"
        )

        print(
            f"Device/Channel Assessment: "
            f"{result.get('assessment', 'N/A')}"
        )

        print("\nFindings:")

        for finding in result.get("findings", []):

            print(
                f"- {finding['signal']} "
                f"[{finding['severity']}]"
            )