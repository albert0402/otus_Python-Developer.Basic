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
    """Create and store a new User instance in the database if it doesn't already exist."""
    existing_user = await session.execute(
        select(User).where(User.username == user_data["username"])
    )
    if existing_user.scalars().first():
        logger.info(f"User {user_data['username']} already exists. Skipping.")
        return None

    user = User(
        name=user_data["name"],
        username=user_data["username"],
        email=user_data["email"]
    )
    session.add(user)
    await session.flush()  # Сохраняем перед коммитом
    await session.commit()
    logger.info(f"User {user_data['username']} added to database.")
    return user

async def create_post(session: AsyncSession, post_data: dict):
    """Create and store a new Post instance in the database."""
    existing_user = await session.execute(
        select(User.id).where(User.id == post_data["userId"])
    )
    user_id = existing_user.scalars().first()

    if not user_id:
        logger.warning(f"User with ID {post_data['userId']} not found. Skipping post.")
        return

    post = Post(
        user_id=user_id,
        title=post_data["title"],
        body=post_data["body"]
    )
    session.add(post)
    await session.flush()
    await session.commit()
    logger.info(f"Post '{post_data['title']}' added to database.")

async def initialize_database():
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized.")

async def main():
    """Main function to fetch data, create users and posts in the database."""
    await initialize_database()
    
    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data()
    )
    
    async with AsyncSessionLocal() as session:
        for user_data in users_data:
            await create_user(session, user_data)

        for post_data in posts_data:
            await create_post(session, post_data)
    
    logger.info("Data successfully inserted into the database.")

if __name__ == "__main__":
    asyncio.run(main())