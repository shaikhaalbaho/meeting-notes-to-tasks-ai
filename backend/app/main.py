from fastapi import FastAPI

from app.routes.extract import router as extract_router

app = FastAPI(
    title="Meeting Notes → Action Items AI",
    description="AI-enhanced API that extracts structured action items from meeting notes",
    version="0.1.0"
)

app.include_router(extract_router)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "meeting-notes-to-tasks-ai",
        "message": "API is running"
    }