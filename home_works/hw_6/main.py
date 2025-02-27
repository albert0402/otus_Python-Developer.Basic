import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import Base, User, Post
from jsonplaceholder_requests import fetch_users_data, fetch_posts_data
from config import db_url, db_echo

# Database connection settings
engine = create_async_engine(db_url, echo=db_echo)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_user(session: AsyncSession, user_data: dict):
    """Creates and saves a user to the database if they do not already exist"""
    existing_user = await session.execute(select(User).where(User.username == user_data["username"]))
    if existing_user.scalars().first():
        logger.info(f"User {user_data['username']} already exists. Skipping.")
        return None

    user = User(
        id=user_data["id"],
        name=user_data["name"],
        username=user_data["username"],
        email=user_data["email"]
    )
    
    session.add(user)
    await session.commit()
    logger.info(f"User {user_data['username']} added to the database.")
    return user

async def create_post(session: AsyncSession, post_data: dict):
    """Creates and saves a post if the user exists"""
    existing_user = await session.execute(select(User.id).where(User.id == post_data["userId"]))
    user_id = existing_user.scalars().first()

    if not user_id:
        logger.warning(f"User with ID {post_data['userId']} not found. Skipping post.")
        return

    existing_post = await session.execute(select(Post).where(Post.id == post_data["id"]))
    if existing_post.scalars().first():
        logger.info(f"Post with ID {post_data['id']} already exists. Skipping.")
        return

    post = Post(
        id=post_data["id"],  # Use the ID from the API
        user_id=user_id,
        title=post_data["title"],
        body=post_data["body"]
    )
    session.add(post)
    await session.commit()
    logger.info(f"Post '{post_data['title']}' added to the database.")

async def save_users_to_db(session: AsyncSession, users_data: list):
    """Adds all users to the database"""
    for user_data in users_data:
        await create_user(session, user_data)
    logger.info(f"Saved {len(users_data)} users to the database.")

async def save_posts_to_db(session: AsyncSession, posts_data: list):
    """Adds all posts to the database"""
    for post_data in posts_data:
        await create_post(session, post_data)
    logger.info(f"Saved {len(posts_data)} posts to the database.")

async def initialize_database():
    """Creates tables in the database if they do not exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized.")

async def main():
    """Main function: loads data and saves it to the database"""
    await initialize_database()

    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data()
    )

    async with AsyncSessionLocal() as session:
        await save_users_to_db(session, users_data)
        await save_posts_to_db(session, posts_data)

    logger.info("Data successfully loaded into the database.")

if __name__ == "__main__":
    asyncio.run(main())