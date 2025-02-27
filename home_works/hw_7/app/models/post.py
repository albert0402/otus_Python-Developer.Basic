from typing import TYPE_CHECKING
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .mixins import CreatedAtMixin

if TYPE_CHECKING:
    from .user import User
    from .tag import Tag


class Post(CreatedAtMixin, Base):
    """Post model representing user posts."""

    __tablename__ = "post"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, default="", server_default="")

    user: Mapped["User"] = relationship(
        back_populates="posts",
    )

    tags: Mapped[list["Tag"]] = relationship(
        secondary="post_tag_association",
        back_populates="posts",
    )

    def __str__(self):
        return f"Post(id={self.id}, title={self.title!r}, user_id={self.user_id})"

    def __repr__(self):
        return self.__str__()
