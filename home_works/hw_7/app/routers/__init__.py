from fastapi import APIRouter
from .users import router as users_router
from .posts import router as posts_router
from .tags import router as tags_router
from .publication_tag_association import router as publication_tags_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(posts_router, prefix="/posts", tags=["Posts"])
router.include_router(tags_router, prefix="/tags", tags=["Tags"])
router.include_router(
    publication_tags_router, prefix="/publication-tags", tags=["Publication Tags"]
)
