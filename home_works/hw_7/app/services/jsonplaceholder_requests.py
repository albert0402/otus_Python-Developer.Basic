import logging
import aiohttp
from typing import List, Dict, Any

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_api(url: str) -> List[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()


async def fetch_users_data() -> List[Dict[str, Any]]:
    data = await fetch_api(USERS_DATA_URL)
    logger.info("Fetched %d users", len(data))
    return data


async def fetch_posts_data() -> List[Dict[str, Any]]:
    data = await fetch_api(POSTS_DATA_URL)
    logger.info("Fetched %d posts", len(data))
    return data
