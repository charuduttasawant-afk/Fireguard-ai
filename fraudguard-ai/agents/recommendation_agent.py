def generate_recommendation(
    risk_result,
    transaction_result=None,
    customer_result=None,
    device_result=None
):

    if not risk_result:
        return {
            "agent": "Recommendation Agent",
            "status": "EXCEPTION",
            "message": "Risk assessment unavailable"
        }

    if risk_result.get("status") != "SUCCESS":
        return {
            "agent": "Recommendation Agent",
            "status": "EXCEPTION",
            "message": "Valid risk assessment is required"
        }

    risk_level = risk_result.get("risk_level")

    risk_score = risk_result.get(
        "risk_score",
        0
    )

    # --------------------------------------------------
    # LOW RISK
    # --------------------------------------------------

    if risk_level == "LOW":

        recommendation = "PROCEED"

        human_review_required = False

        escalation_required = False

        rationale = (
            "Available evidence indicates low fraud risk. "
            "No immediate human intervention is required."
        )

    # --------------------------------------------------
    # MEDIUM RISK
    # --------------------------------------------------

    elif risk_level == "MEDIUM":

        recommendation = "HUMAN_REVIEW"

        human_review_required = True

        escalation_required = False

        rationale = (
            "Evidence contains potentially suspicious "
            "signals or ambiguity. Human investigator "
            "review is required before a consequential action."
        )

    # --------------------------------------------------
    # HIGH RISK
    # --------------------------------------------------

    elif risk_level == "HIGH":

        recommendation = "ESCALATE"

        human_review_required = True

        escalation_required = True

        rationale = (
            "Multiple high-risk indicators are present. "
            "The case should be escalated to the appropriate "
            "fraud investigation team for human decision."
        )

    # --------------------------------------------------
    # UNKNOWN RISK
    # --------------------------------------------------

    else:

        recommendation = "HUMAN_REVIEW"

        human_review_required = True

        escalation_required = False

        rationale = (
            "Risk level could not be reliably determined. "
            "Human review is required."
        )

    return {
        "agent": "Recommendation Agent",
        "status": "SUCCESS",
        "risk_level": risk_level,
        "risk_score": risk_score,
        "recommendation": recommendation,
        "human_review_required": human_review_required,
        "escalation_required": escalation_required,
        "rationale": rationale
    }


# ------------------------------------------------------
# TEST THE AGENT
# ------------------------------------------------------

if __name__ == "__main__":

    test_risk_results = [

        {
            "status": "SUCCESS",
            "risk_level": "LOW",
            "risk_score": 0
        },

        {
            "status": "SUCCESS",
            "risk_level": "MEDIUM",
            "risk_score": 45
        },

        {
            "status": "SUCCESS",
            "risk_level": "HIGH",
            "risk_score": 80
        }
    ]

    for risk_result in test_risk_results:

        print("\n" + "=" * 60)

        result = generate_recommendation(
            risk_result
        )

        print(
            f"Risk Level: "
            f"{result['risk_level']}"
        )

        print(
            f"Recommendation: "
            f"{result['recommendation']}"
        )

        print(
            f"Human Review: "
            f"{result['human_review_required']}"
        )

        print(
            f"Escalation: "
            f"{result['escalation_required']}"
        )

        print(
            f"Rationale: "
            f"{result['rationale']}"
        )