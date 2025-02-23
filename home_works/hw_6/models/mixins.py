from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class CreatedAtMixin:
    """Mixin for adding created_at timestamp to models."""

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )