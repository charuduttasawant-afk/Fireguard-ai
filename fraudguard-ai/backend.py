from fastapi import FastAPI
from pydantic import BaseModel

from agents.transaction_agent import analyze_transaction
from agents.customer_agent import analyze_customer_behavior
from agents.device_agent import analyze_device_behavior
from agents.risk_agent import analyze_transaction as analyze_risk
from agents.recommendation_agent import generate_recommendation


app = FastAPI(
    title="FraudGuard AI Backend"
)


class InvestigationRequest(BaseModel):
    transaction_id: str


@app.get("/")
def root():

    return {
        "service": "FraudGuard AI Backend",
        "status": "running"
    }


@app.post("/investigate")
def investigate(
    request: InvestigationRequest
):

    transaction_id = request.transaction_id

    transaction_result = analyze_transaction(
        transaction_id
    )

    customer_result = analyze_customer_behavior(
        transaction_id
    )

    device_result = analyze_device_behavior(
        transaction_id
    )

    risk_result = analyze_risk(
        transaction_id
    )

    recommendation_result = generate_recommendation(
        risk_result,
        transaction_result,
        customer_result,
        device_result
    )

    return {

        "transaction": transaction_result,

        "customer": customer_result,

        "device": device_result,

        "risk": risk_result,

        "recommendation": recommendation_result
    }