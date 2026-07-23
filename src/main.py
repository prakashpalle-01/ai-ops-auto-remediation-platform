from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect

from src.models import AlertCreate, RemediationRequest, RemediationResponse
from src.store import AlertStore

app = FastAPI(title="AI Ops & Auto-Remediation Platform")
store = AlertStore()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/alerts")
def ingest_alert(payload: AlertCreate):
    return store.add_alert(payload)


@app.get("/alerts/{alert_id}", responses={404: {"description": "Alert not found"}})
def get_alert(alert_id: str):
    alert = store.get_alert(alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.post("/remediate")
def remediate_alert(payload: RemediationRequest) -> RemediationResponse:
    return store.remediate(payload.alert_id)


@app.websocket("/ws/alerts")
async def alert_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_json({"event": "alert_received", "message": message})
    except WebSocketDisconnect:
        return
