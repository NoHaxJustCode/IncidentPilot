from fastapi import FastAPI

app = FastAPI(title="IncidentPilot")

@app.get("/health")
def health():
    return {"status": "ok"}
