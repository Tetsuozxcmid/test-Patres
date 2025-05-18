from fastapi import FastAPI
from core.logger import logger

app = FastAPI(
    title="FastAPI",
    description="ыфвфвфвф))",
    docs_url="/",
   
)

logger.info("Запускаем...")

@app.on_event("startup")
async def startup_event():
    logger.info("Приложение запущено")