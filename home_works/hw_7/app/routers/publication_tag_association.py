from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.publication_tag_association import PostTagAssociation
from app.services.database import get_db

router = APIRouter()


@router.get("/")
async def get_publication_tag_association(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PostTagAssociation))
    return result.scalars().all()
