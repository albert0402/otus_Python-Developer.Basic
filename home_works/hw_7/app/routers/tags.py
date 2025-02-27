from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.tag import Tag
from app.services.database import get_db

router = APIRouter()

@router.get("/")
async def get_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag))
    tags = result.scalars().all()
    return tags