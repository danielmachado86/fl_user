from motor.motor_asyncio import AsyncIOMotorClient
import logging

from api.config import settings

logging.basicConfig(level=logging.DEBUG)


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    logging.info("Opening database connection...")
    db.client = AsyncIOMotorClient(
        str(settings.MONGODB_URL),
        maxPoolSize=settings.MAX_CONNECTIONS_COUNT,
        minPoolSize=settings.MIN_CONNECTIONS_COUNT,
    )
    logging.info("Database connected")


async def close_mongo_connection():
    logging.info("Closing database connection...")
    db.client.close()
    logging.info("Database closed")
