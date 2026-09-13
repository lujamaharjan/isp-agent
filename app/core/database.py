import bcrypt
from sqlalchemy import Column, String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import DATABASE_URL

Base = declarative_base()

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class AppUser(Base):
    __tablename__ = "credentials"

    username = Column(String, primary_key=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


async def get_user(username: str) -> AppUser | None:
    async with async_session() as session:
        result = await session.execute(select(AppUser).where(AppUser.username == username))
        return result.scalar_one_or_none()


async def create_user(username: str, password: str, role: str = "user") -> AppUser:
    async with async_session() as session:
        user = AppUser(username=username, password_hash=hash_password(password), role=role)
        session.add(user)
        await session.commit()
        return user


async def authenticate(username: str, password: str) -> AppUser | None:
    user = await get_user(username)
    if user and verify_password(password, user.password_hash):
        return user
    return None
