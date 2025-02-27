import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import Base, User, Post
from services.jsonplaceholder_requests import fetch_users_data, fetch_posts_data
from services.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_user(session: AsyncSession, user_data: dict):
    existing_user = await session.execute(select(User).where(User.username == user_data["username"]))
    if existing_user.scalars().first():
        return

    user = User(id=user_data["id"], name=user_data["name"], username=user_data["username"], email=user_data["email"])
    session.add(user)
    await session.commit()

async def create_post(session: AsyncSession, post_data: dict):
    existing_user = await session.execute(select(User.id).where(User.id == post_data["userId"]))
    user_id = existing_user.scalars().first()

    if not user_id:
        return

    post = Post(id=post_data["id"], user_id=user_id, title=post_data["title"], body=post_data["body"])
    session.add(post)
    await session.commit()

async def save_users_to_db(session: AsyncSession, users_data: list):
    for user_data in users_data:
        await create_user(session, user_data)

async def save_posts_to_db(session: AsyncSession, posts_data: list):
    for post_data in posts_data:
        await create_post(session, post_data)

async def initialize_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await initialize_database()
    users_data, posts_data = await asyncio.gather(fetch_users_data(), fetch_posts_data())

    async with AsyncSessionLocal() as session:
        await save_users_to_db(session, users_data)
        await save_posts_to_db(session, posts_data)

if __name__ == "__main__":
    asyncio.run(main())
