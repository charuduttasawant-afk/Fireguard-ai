import streamlit as st
import requests


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide"
)


# ======================================================
# CONFIGURATION
# ======================================================

BACKEND_URL = "http://localhost:8000"
# N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/YOUR_WEBHOOK_PATH"


# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    color: #888888;
    margin-top: 0px;
}

.risk-low {
    padding: 15px;
    border-radius: 10px;
    background-color: #d4edda;
    color: #155724;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
}

.risk-medium {
    padding: 15px;
    border-radius: 10px;
    background-color: #fff3cd;
    color: #856404;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
}

.risk-high {
    padding: 15px;
    border-radius: 10px;
    background-color: #f8d7da;
    color: #721c24;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
}

.section-header {
    font-size: 24px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ======================================================
# HEADER
# ======================================================

st.markdown(
    '<div class="main-title">🛡️ FraudGuard AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Governed Agentic AI for Banking Fraud Investigation'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "FraudGuard AI investigates transactions using multiple specialized "
    "AI agents and provides a risk-based recommendation. "
    "Humans remain responsible for consequential decisions."
)

st.divider()


# ======================================================
# BACKEND HEALTH CHECK
# ======================================================

with st.sidebar:

    st.header("⚙️ System")

    try:

        response = requests.post(
    f"{BACKEND_URL}/investigate",
    json={
        "transaction_id": transaction_id
    },
    timeout=30
)

        if response.status_code == 200:
            st.success("🟢 FastAPI Backend Online")
        else:
            st.warning("🟡 Backend Responding")

    except Exception:
        st.error("🔴 FastAPI Backend Offline")

    st.caption(
        f"Backend: {BACKEND_URL}"
    )


# ======================================================
# TRANSACTION INPUT
# ======================================================

st.header("🔍 Fraud Investigation")

transaction_id = st.text_input(
    "Enter Transaction ID",
    value="TXN1001",
    placeholder="Example: TXN1001"
)

st.caption(
    "Available demo transactions: TXN1001, TXN1002, TXN1003"
)


investigate = st.button(
    "🔎 Investigate Transaction",
    type="primary",
    use_container_width=True
)


# ======================================================
# INVESTIGATION
# ======================================================

if investigate:

    if not transaction_id.strip():

        st.error("Please enter a Transaction ID.")

        st.stop()

    transaction_id = transaction_id.strip().upper()

    with st.spinner(
        "FraudGuard AI is analyzing the transaction..."
    ):

        try:

            response = requests.post(
                f"{BACKEND_URL}/investigate",
                json={
                    "transaction_id": transaction_id
                },
                timeout=30
            )

            response.raise_for_status()

            result = response.json()

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to the FastAPI backend. "
                "Make sure Uvicorn is running on port 8000."
            )

            st.stop()

        except requests.exceptions.Timeout:

            st.error(
                "The investigation timed out."
            )

            st.stop()

        except requests.exceptions.HTTPError as error:

            st.error(
                f"Backend returned an error: {error}"
            )

            st.stop()

        except Exception as error:

            st.error(
                f"Unexpected error: {error}"
            )

            st.stop()


    # ==================================================
    # EXTRACT RESULTS
    # ==================================================

    transaction_result = result.get(
        "transaction",
        {}
    )

    customer_result = result.get(
        "customer",
        {}
    )

    device_result = result.get(
        "device",
        {}
    )

    risk_result = result.get(
        "risk",
        {}
    )

    recommendation_result = result.get(
        "recommendation",
        {}
    )


    # ==================================================
    # CHECK INVESTIGATION STATUS
    # ==================================================

    if transaction_result.get("status") != "SUCCESS":

        st.error(
            transaction_result.get(
                "message",
                "Transaction investigation failed."
            )
        )

        st.stop()


    st.success(
        f"Investigation completed for {transaction_id}"
    )


    # ==================================================
    # TRANSACTION DETAILS
    # ==================================================

    st.divider()

    st.header("💳 Transaction Details")

    transaction_data = transaction_result.get(
        "transaction",
        {}
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Transaction",
            transaction_id
        )

    with col2:
        st.metric(
            "Amount",
            f"₹{transaction_data.get('amount', 0):,}"
        )

    with col3:
        st.metric(
            "Location",
            transaction_data.get(
                "location",
                "N/A"
            )
        )

    with col4:
        st.metric(
            "Channel",
            transaction_data.get(
                "channel",
                "N/A"
            )
        )


    # ==================================================
    # RISK ASSESSMENT
    # ==================================================

    st.divider()

    st.header("🚨 Risk Assessment")

    risk_level = risk_result.get(
        "risk_level",
        "UNKNOWN"
    )

    risk_score = risk_result.get(
        "risk_score",
        0
    )

    human_review = risk_result.get(
        "human_review_required",
        False
    )

    escalation = risk_result.get(
        "escalation_required",
        False
    )

    recommendation = recommendation_result.get(
        "recommendation",
        "HUMAN_REVIEW"
    )


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Risk Score",
            risk_score
        )

    with col2:

        st.metric(
            "Risk Level",
            risk_level
        )

    with col3:

        st.metric(
            "Human Review",
            "YES" if human_review else "NO"
        )

    with col4:

        st.metric(
            "Escalation",
            "YES" if escalation else "NO"
        )


    # Risk banner

    if risk_level == "LOW":

        st.markdown(
            '<div class="risk-low">'
            '🟢 LOW RISK'
            '</div>',
            unsafe_allow_html=True
        )

    elif risk_level == "MEDIUM":

        st.markdown(
            '<div class="risk-medium">'
            '🟡 MEDIUM RISK'
            '</div>',
            unsafe_allow_html=True
        )

    elif risk_level == "HIGH":

        st.markdown(
            '<div class="risk-high">'
            '🔴 HIGH RISK'
            '</div>',
            unsafe_allow_html=True
        )


    # ==================================================
    # RECOMMENDATION
    # ==================================================

    st.subheader("🎯 AI Recommendation")

    if recommendation == "PROCEED":

        st.success(
            "✅ PROCEED"
        )

    elif recommendation == "HUMAN_REVIEW":

        st.warning(
            "⚠️ HUMAN REVIEW REQUIRED"
        )

    else:

        st.error(
            f"🚨 {recommendation}"
        )

    st.info(
        recommendation_result.get(
            "rationale",
            "No rationale available."
        )
    )


    # ==================================================
    # RISK FINDINGS
    # ==================================================

    st.divider()

    st.header("⚠️ Risk Findings")

    findings = risk_result.get(
        "findings",
        []
    )

    if findings:

        for finding in findings:

            rule = finding.get(
                "rule",
                "N/A"
            )

            signal = finding.get(
                "signal",
                "Unknown"
            )

            points = finding.get(
                "risk_points",
                0
            )

            description = finding.get(
                "description",
                ""
            )

            st.write(
                f"**{rule} — {signal}** "
                f"**(+{points} points)**"
            )

            st.caption(description)

            st.divider()

    else:

        st.success(
            "No significant risk signals detected."
        )


    # ==================================================
    # AGENT EVIDENCE
    # ==================================================

    st.header("🤖 Agent Evidence")


    # ----------------------------------------------
    # Transaction Agent
    # ----------------------------------------------

    with st.expander(
        "1️⃣ Transaction Analysis Agent",
        expanded=True
    ):

        st.write(
            f"Assessment: "
            f"**{transaction_result.get('assessment', 'N/A')}**"
        )

        for finding in transaction_result.get(
            "findings",
            []
        ):

            st.write(
                f"**{finding.get('signal', 'N/A')}** — "
                f"{finding.get('description', '')}"
            )


    # ----------------------------------------------
    # Customer Agent
    # ----------------------------------------------

    with st.expander(
        "2️⃣ Customer Behaviour Agent"
    ):

        st.write(
            f"Assessment: "
            f"**{customer_result.get('assessment', 'N/A')}**"
        )

        for finding in customer_result.get(
            "findings",
            []
        ):

            st.write(
                f"**{finding.get('signal', 'N/A')}** — "
                f"{finding.get('description', '')}"
            )


    # ----------------------------------------------
    # Device Agent
    # ----------------------------------------------

    with st.expander(
        "3️⃣ Device / Channel Agent"
    ):

        st.write(
            f"Assessment: "
            f"**{device_result.get('assessment', 'N/A')}**"
        )

        for finding in device_result.get(
            "findings",
            []
        ):

            st.write(
                f"**{finding.get('signal', 'N/A')}** — "
                f"{finding.get('description', '')}"
            )


    # ----------------------------------------------
    # Risk Agent
    # ----------------------------------------------

    with st.expander(
        "4️⃣ Risk / Policy Agent"
    ):

        st.write(
            f"Risk Score: "
            f"**{risk_score}**"
        )

        st.write(
            f"Risk Level: "
            f"**{risk_level}**"
        )

        for finding in risk_result.get(
            "findings",
            []
        ):

            st.write(
                f"**{finding.get('signal', 'N/A')}** — "
                f"{finding.get('description', '')}"
            )


    # ----------------------------------------------
    # Recommendation Agent
    # ----------------------------------------------

    with st.expander(
        "5️⃣ Recommendation Agent"
    ):

        st.write(
            f"Recommendation: "
            f"**{recommendation}**"
        )

        st.write(
            recommendation_result.get(
                "rationale",
                "No rationale available."
            )
        )


    # ==================================================
    # GOVERNANCE
    # ==================================================

    st.divider()

    st.header("🛡️ Governance & Human Oversight")

    gov_col1, gov_col2 = st.columns(2)

    with gov_col1:

        if human_review:

            st.warning(
                "⚠️ Human review is required before "
                "a consequential decision."
            )

        else:

            st.success(
                "✅ No human review is currently required."
            )


    with gov_col2:

        if escalation:

            st.error(
                "🚨 Escalation is required."
            )

        else:

            st.info(
                "No escalation required."
            )


    # ==================================================
    # AUDIT SUMMARY
    # ==================================================

    st.divider()

    st.header("📋 Investigation Audit Summary")

    audit_data = {
        "Transaction ID": transaction_id,
        "Risk Score": risk_score,
        "Risk Level": risk_level,
        "Recommendation": recommendation,
        "Human Review":
            "Required" if human_review
            else "Not Required",
        "Escalation":
            "Required" if escalation
            else "Not Required"
    }

    for key, value in audit_data.items():

        st.write(
            f"**{key}:** {value}"
        )