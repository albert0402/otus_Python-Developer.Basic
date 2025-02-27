from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT
from .base import Base
from .mixins import CreatedAtMixin

if TYPE_CHECKING:
    from .post import Post


class Tag(CreatedAtMixin, Base):
    """Tag model representing tags associated with posts."""

    __tablename__ = "tag"

    name: Mapped[str] = mapped_column(CITEXT, unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        secondary="post_tag_association",
        back_populates="tags",
    )

    def __str__(self) -> str:
        return f"Tag(id={self.id!r}, name={self.name!r})"

    def __repr__(self) -> str:
        return self.__str__()
