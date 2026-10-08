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

FASTAPI_URL = "https://fireguard-ai-production.up.railway.app/investigate"


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
    "FraudGuard AI investigates transactions using multiple "
    "specialized AI agents and provides a risk-based recommendation. "
    "Humans remain responsible for consequential decisions."
)

st.divider()


# ======================================================
# SIDEBAR / SYSTEM STATUS
# ======================================================

with st.sidebar:

    st.header("⚙️ System")

    st.success("🟢 Cloud Backend Connected")

    st.caption(
        f"Backend: {FASTAPI_URL}"
    )

    st.divider()

    st.markdown("### Architecture")

    st.caption(
        "Streamlit → Railway FastAPI → AI Agents"
    )

    st.divider()

    st.markdown("### Demo Transactions")

    st.caption(
        "TXN1001 → LOW"
    )

    st.caption(
        "TXN1002 → MEDIUM"
    )

    st.caption(
        "TXN1003 → HIGH"
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

        st.error(
            "Please enter a Transaction ID."
        )

        st.stop()

    transaction_id = transaction_id.strip().upper()

    with st.spinner(
        "FraudGuard AI is analyzing the transaction..."
    ):

        try:

            response = requests.post(
                FASTAPI_URL,
                json={
                    "transaction_id": transaction_id
                },
                timeout=120
            )

            # --------------------------------------------------
            # HTTP ERROR
            # --------------------------------------------------

            if response.status_code != 200:

                st.error(
                    f"🔴 Backend returned HTTP "
                    f"{response.status_code}: "
                    f"{response.text}"
                )

                st.stop()

            # --------------------------------------------------
            # PARSE JSON
            # --------------------------------------------------

            result = response.json()

        except requests.exceptions.ConnectionError:

            st.error(
                "🔴 Cannot connect to the Railway FastAPI backend."
            )

            st.caption(
                f"Backend URL: {FASTAPI_URL}"
            )

            st.stop()

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The FastAPI investigation timed out."
            )

            st.stop()

        except ValueError:

            st.error(
                "🔴 FastAPI returned a response that "
                "was not valid JSON."
            )

            st.stop()

        except Exception as error:

            st.error(
                f"🔴 Unexpected backend error: {error}"
            )

            st.stop()


    # ==================================================
    # EXTRACT FASTAPI RESPONSE
    # ==================================================

    transaction_data = result.get(
        "transaction",
        {}
    )

    customer_data = result.get(
        "customer",
        {}
    )

    device_data = result.get(
        "device",
        {}
    )

    risk_data = result.get(
        "risk",
        {}
    )

    recommendation_data = result.get(
        "recommendation",
        {}
    )


    # ==================================================
    # EXTRACT RISK INFORMATION
    # ==================================================

    status = risk_data.get(
        "status",
        "SUCCESS"
    )

    risk_level = str(
        risk_data.get(
            "risk_level",
            "UNKNOWN"
        )
    ).upper()

    risk_score = risk_data.get(
        "risk_score",
        0
    )

    human_review = bool(
        risk_data.get(
            "human_review_required",
            False
        )
    )

    escalation = bool(
        risk_data.get(
            "escalation_required",
            False
        )
    )


    # ==================================================
    # EXTRACT RECOMMENDATION
    # ==================================================

    recommendation = str(
        recommendation_data.get(
            "recommendation",
            "UNKNOWN"
        )
    ).upper()

    message = recommendation_data.get(
        "rationale",
        "Transaction assessed successfully."
    )


    # ==================================================
    # CHECK STATUS
    # ==================================================

    if status not in (
        "SUCCESS",
        "COMPLETED"
    ):

        st.error(
            message
        )

        st.stop()


    # ==================================================
    # SUCCESS
    # ==================================================

    st.success(
        f"🟢 Investigation completed for "
        f"{transaction_id}"
    )


    # ==================================================
    # RAW FASTAPI RESPONSE
    # ==================================================

    with st.expander(
        "🔎 View Complete API Response"
    ):

        st.json(result)


    # ==================================================
    # TRANSACTION DETAILS
    # ==================================================

    st.divider()

    st.header(
        "💳 Transaction Details"
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Transaction",
            transaction_id
        )


    with col2:

        st.metric(
            "Risk Score",
            risk_score
        )


    with col3:

        st.metric(
            "Risk Level",
            risk_level
        )


    with col4:

        st.metric(
            "Decision",
            recommendation
        )


    # ==================================================
    # TRANSACTION INFORMATION
    # ==================================================

    transaction_details = transaction_data.get(
        "transaction",
        {}
    )

    st.subheader(
        "Transaction Information"
    )

    tx_col1, tx_col2, tx_col3, tx_col4 = st.columns(4)


    with tx_col1:

        st.metric(
            "Amount",
            f"₹{transaction_details.get('amount', 'N/A')}"
        )


    with tx_col2:

        st.metric(
            "Merchant",
            transaction_details.get(
                "merchant",
                "N/A"
            )
        )


    with tx_col3:

        st.metric(
            "Location",
            transaction_details.get(
                "location",
                "N/A"
            )
        )


    with tx_col4:

        st.metric(
            "Channel",
            transaction_details.get(
                "channel",
                "N/A"
            )
        )


    # ==================================================
    # RISK ASSESSMENT
    # ==================================================

    st.divider()

    st.header(
        "🚨 Risk Assessment"
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


    # ==================================================
    # RISK BANNER
    # ==================================================

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
    # AI RECOMMENDATION
    # ==================================================

    st.subheader(
        "🎯 AI Recommendation"
    )


    if recommendation == "PROCEED":

        st.success(
            "✅ PROCEED"
        )

    elif recommendation == "HUMAN_REVIEW":

        st.warning(
            "⚠️ HUMAN REVIEW REQUIRED"
        )

    elif recommendation == "ESCALATE":

        st.error(
            "🚨 ESCALATE"
        )

    else:

        st.error(
            f"🚨 {recommendation}"
        )


    st.info(
        message
    )


    # ==================================================
    # GOVERNANCE
    # ==================================================

    st.divider()

    st.header(
        "🛡️ Governance & Human Oversight"
    )

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
    # AGENT EVIDENCE
    # ==================================================

    st.divider()

    st.header(
        "🤖 Agent Evidence"
    )

    st.caption(
        "FraudGuard AI uses specialized agents for "
        "transaction analysis, customer behaviour, "
        "device/channel analysis, risk assessment, "
        "and recommendation."
    )


    # ==================================================
    # 1. TRANSACTION AGENT
    # ==================================================

    with st.expander(
        "1️⃣ Transaction Analysis Agent",
        expanded=True
    ):

        st.write(
            f"**Assessment:** "
            f"{transaction_data.get('assessment', 'N/A')}"
        )

        st.write(
            f"**Agent Status:** "
            f"{transaction_data.get('status', 'N/A')}"
        )

        st.write(
            f"**Transaction ID:** "
            f"{transaction_data.get('transaction_id', transaction_id)}"
        )

        st.write(
            "**Findings:**"
        )

        transaction_findings = transaction_data.get(
            "findings",
            []
        )

        if transaction_findings:

            for finding in transaction_findings:

                severity = finding.get(
                    "severity",
                    "INFO"
                )

                signal = finding.get(
                    "signal",
                    "Signal"
                )

                description = finding.get(
                    "description",
                    ""
                )

                st.write(
                    f"• **{signal}** "
                    f"({severity}) — "
                    f"{description}"
                )

        else:

            st.info(
                "No transaction findings."
            )


    # ==================================================
    # 2. CUSTOMER AGENT
    # ==================================================

    with st.expander(
        "2️⃣ Customer Behaviour Agent"
    ):

        st.write(
            f"**Customer ID:** "
            f"{customer_data.get('customer_id', 'N/A')}"
        )

        st.write(
            f"**Assessment:** "
            f"{customer_data.get('assessment', 'N/A')}"
        )

        profile = customer_data.get(
            "customer_profile",
            {}
        )

        profile_col1, profile_col2 = st.columns(2)


        with profile_col1:

            st.write(
                f"**Usual Location:** "
                f"{profile.get('usual_location', 'N/A')}"
            )

            st.write(
                f"**Usual Channel:** "
                f"{profile.get('usual_channel', 'N/A')}"
            )

            st.write(
                f"**Usual Device:** "
                f"{profile.get('usual_device', 'N/A')}"
            )


        with profile_col2:

            st.write(
                f"**Average Transaction:** "
                f"₹{profile.get('average_transaction', 'N/A')}"
            )

            travel_history = profile.get(
                "travel_history",
                []
            )

            st.write(
                f"**Travel History:** "
                f"{len(travel_history)} record(s)"
            )


        st.write(
            "**Behavioural Findings:**"
        )

        customer_findings = customer_data.get(
            "findings",
            []
        )

        if customer_findings:

            for finding in customer_findings:

                severity = finding.get(
                    "severity",
                    "INFO"
                )

                signal = finding.get(
                    "signal",
                    "Signal"
                )

                description = finding.get(
                    "description",
                    ""
                )

                st.write(
                    f"• **{signal}** "
                    f"({severity}) — "
                    f"{description}"
                )

        else:

            st.info(
                "No customer findings."
            )


    # ==================================================
    # 3. DEVICE AGENT
    # ==================================================

    with st.expander(
        "3️⃣ Device / Channel Agent"
    ):

        st.write(
            f"**Customer ID:** "
            f"{device_data.get('customer_id', 'N/A')}"
        )

        st.write(
            f"**Assessment:** "
            f"{device_data.get('assessment', 'N/A')}"
        )

        device_profile = device_data.get(
            "device_profile",
            {}
        )

        device_col1, device_col2 = st.columns(2)


        with device_col1:

            st.write(
                f"**Device ID:** "
                f"{device_profile.get('device_id', 'N/A')}"
            )

            st.write(
                f"**Known Device:** "
                f"{'YES' if device_profile.get('known_device') else 'NO'}"
            )


        with device_col2:

            st.write(
                f"**Device Customer:** "
                f"{device_profile.get('device_customer_id', 'N/A')}"
            )

            st.write(
                f"**Transaction Channel:** "
                f"{device_profile.get('transaction_channel', 'N/A')}"
            )

            st.write(
                f"**Usual Channel:** "
                f"{device_profile.get('usual_channel', 'N/A')}"
            )


        st.write(
            "**Device Findings:**"
        )

        device_findings = device_data.get(
            "findings",
            []
        )

        if device_findings:

            for finding in device_findings:

                severity = finding.get(
                    "severity",
                    "INFO"
                )

                signal = finding.get(
                    "signal",
                    "Signal"
                )

                description = finding.get(
                    "description",
                    ""
                )

                st.write(
                    f"• **{signal}** "
                    f"({severity}) — "
                    f"{description}"
                )

        else:

            st.info(
                "No device findings."
            )


    # ==================================================
    # 4. RISK AGENT
    # ==================================================

    with st.expander(
        "4️⃣ Risk / Policy Agent"
    ):

        risk_col1, risk_col2 = st.columns(2)


        with risk_col1:

            st.write(
                f"**Risk Score:** "
                f"**{risk_score}**"
            )

            st.write(
                f"**Risk Level:** "
                f"**{risk_level}**"
            )


        with risk_col2:

            st.write(
                f"**Human Review:** "
                f"**{'YES' if human_review else 'NO'}**"
            )

            st.write(
                f"**Escalation:** "
                f"**{'YES' if escalation else 'NO'}**"
            )


        risk_findings = risk_data.get(
            "findings",
            []
        )

        st.write(
            "**Risk Findings:**"
        )

        if risk_findings:

            for finding in risk_findings:

                if isinstance(finding, dict):

                    rule = finding.get(
                        "rule",
                        finding.get(
                            "signal",
                            "Risk Rule"
                        )
                    )

                    description = finding.get(
                        "description",
                        ""
                    )

                    points = finding.get(
                        "points",
                        finding.get(
                            "score",
                            ""
                        )
                    )

                    if points != "":

                        st.write(
                            f"• **{rule}** "
                            f"(+{points}) — "
                            f"{description}"
                        )

                    else:

                        st.write(
                            f"• **{rule}** — "
                            f"{description}"
                        )

                else:

                    st.write(
                        f"• {finding}"
                    )

        else:

            st.success(
                "No additional risk findings."
            )


    # ==================================================
    # 5. RECOMMENDATION AGENT
    # ==================================================

    with st.expander(
        "5️⃣ Recommendation Agent"
    ):

        st.write(
            f"**Recommendation:** "
            f"**{recommendation}**"
        )

        st.write(
            f"**Risk Level:** "
            f"{recommendation_data.get('risk_level', risk_level)}"
        )

        st.write(
            f"**Risk Score:** "
            f"{recommendation_data.get('risk_score', risk_score)}"
        )

        st.write(
            f"**Human Review Required:** "
            f"{'YES' if recommendation_data.get('human_review_required', human_review) else 'NO'}"
        )

        st.write(
            f"**Escalation Required:** "
            f"{'YES' if recommendation_data.get('escalation_required', escalation) else 'NO'}"
        )

        st.write(
            "**Rationale:**"
        )

        st.info(
            recommendation_data.get(
                "rationale",
                message
            )
        )


    # ==================================================
    # AUDIT SUMMARY
    # ==================================================

    st.divider()

    st.header(
        "📋 Investigation Audit Summary"
    )

    audit_data = {

        "Transaction ID":
            transaction_id,

        "Risk Score":
            risk_score,

        "Risk Level":
            risk_level,

        "Recommendation":
            recommendation,

        "Human Review":
            "Required"
            if human_review
            else "Not Required",

        "Escalation":
            "Required"
            if escalation
            else "Not Required",

        "Status":
            status
    }


    for key, value in audit_data.items():

        st.write(
            f"**{key}:** {value}"
        )