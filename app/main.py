from fastapi import FastAPI

app = FastAPI(title="Multi-Agent System")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
