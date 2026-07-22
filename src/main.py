from fastapi import FastAPI

app = FastAPI(title="AI Ops & Auto-Remediation Platform")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
