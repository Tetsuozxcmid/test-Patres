from fastapi import FastAPI
from core.logger import logger
from api.v1.admins.router import router as auth_router

app = FastAPI(
    title="FastAPI",
    description="ыфвфвфвф))",
    docs_url="/",
   
)

app.include_router(auth_router)

logger.info("Запускаем...")

@app.on_event("startup")
async def startup_event():
    logger.info("Приложение запущено")