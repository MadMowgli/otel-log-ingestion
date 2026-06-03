from fastapi import FastAPI
from util.setup_logger import setup_logging

app = FastAPI()
logger = setup_logging('otel-logs-ingestion-app')

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Hello World"}
