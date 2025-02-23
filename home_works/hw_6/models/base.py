from sqlalchemy import create_engine, event, MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from config import db_url, convention


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    metadata = MetaData(naming_convention=convention)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Automatically sets table name to lowercase class name."""
        return cls.__name__.lower()


engine = create_engine(
    db_url,
    echo=True,  # Enable echo for debugging
)


def set_foreign_keys_on(dbapi_conn, connection_record):
    """Enable foreign key constraints for SQLite."""
    if "sqlite:///" not in db_url:
        return
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.close()


event.listen(engine, "connect", set_foreign_keys_on)