from fastapi import FastAPI

from api import close_mongo_connection, connect_to_mongo
from api.config import settings
from api.endpoints import router as api_router


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, debug=True)
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(api_router, prefix=settings.API_V1_STR)
