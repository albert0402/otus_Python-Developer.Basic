from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .post import Post


class User(Base):
    """User model representing system users."""

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        nullable=False
    )
    
    email: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        nullable=False
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"

    def __repr__(self):
        return self.__str__()