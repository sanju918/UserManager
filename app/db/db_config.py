from dotenv import dotenv_values
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

db_user = dotenv_values("PG_USER")
db_pwd = dotenv_values("PG_PWD")
db_name = dotenv_values("PG_DB_NAME")

DB_URL = f"postgresql+asyncpg://{db_user}:{db_pwd}@localhost:5432/{db_name}"

engine = create_async_engine(DB_URL, echo=True, future=True)
session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)()

Base = declarative_base()


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def commit_rollback():
    try:
        async with session as db:
            yield db
            await db.commit()
    except Exception:
        await db.rollback()
        raise
