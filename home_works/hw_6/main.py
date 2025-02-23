import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import Base, User, Post
from jsonplaceholder_requests import fetch_users_data, fetch_posts_data
from config import db_url, db_echo

# Database connection settings
logger = logging.getLogger(__name__)
logger.info(f"Connecting to database with URL: {db_url}")
engine = create_async_engine(db_url, echo=db_echo)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Logging setup
logging.basicConfig(level=logging.INFO)

async def create_user(session: AsyncSession, user_data: dict):
    """Create and store a new User instance in the database if it doesn't already exist."""
    # Проверяем, существует ли пользователь с таким username
    existing_user = await session.execute(
        select(User).where(User.username == user_data["username"])
    )
    if existing_user.scalar():
        logger.info(f"User with username {user_data['username']} already exists. Skipping insertion.")
        return None

    # Если пользователя нет, создаем нового
    user = User(
        name=user_data["name"],
        username=user_data["username"],
        email=user_data["email"]
    )
    session.add(user)
    await session.commit()
    return user

async def create_post(session: AsyncSession, post_data: dict):
    """Create and store a new Post instance in the database."""
    post = Post(
        user_id=post_data["userId"],
        title=post_data["title"],
        body=post_data["body"]
    )
    session.add(post)
    await session.commit()
    return post

async def initialize_database():
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    """Main function to fetch data, create users and posts in the database."""
    await initialize_database()
    
    # Fetch users and posts concurrently
    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data()
    )
    
    # Store users and posts in the database
    async with AsyncSessionLocal() as session:
        # Создаем пользователей
        for user_data in users_data:
            await create_user(session, user_data)
        
        # Создаем посты
        for post_data in posts_data:
            await create_post(session, post_data)
    
    logger.info("Data successfully inserted into the database.")

if __name__ == "__main__":
    asyncio.run(main())