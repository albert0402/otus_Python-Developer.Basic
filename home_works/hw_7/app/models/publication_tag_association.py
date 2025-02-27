from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class PostTagAssociation(Base):
    """Association table for the many-to-many relationship between Post and Tag."""

    __tablename__ = "post_tag_association"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), nullable=False)

    __table_args__ = (UniqueConstraint("post_id", "tag_id"),)