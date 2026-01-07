from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import datetime


class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        comment="create time"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
        comment="update time"
    )

class Category(Base):
    __tablename__ = "new_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="category id")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="category name")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="sort order")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"