from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pyprojroot import here
import sys
sys.path.append(str(here()))

from config import settings

async_engine = create_async_engine(settings.mysql_url, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

async def get_db():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()