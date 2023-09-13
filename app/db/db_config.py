from dotenv import dotenv_values
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

db_details = dotenv_values(".env")
db_user = db_details["PG_USER"]
db_pwd = db_details["PG_PWD"]
db_name = db_details["PG_DB_NAME"]
# print(db_name, db_pwd, db_user)
DB_URL = f"postgresql+asyncpg://{db_user}:{db_pwd}@localhost:5432/{db_name}"

engine = create_async_engine(DB_URL, echo=True, future=True)
session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)()

Base = declarative_base()


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_async_db():
    async with session as async_db:
        yield async_db
        try:
            await async_db.commit()
        except Exception:
            await async_db.rollback()
            raise
