from typing import Optional

from sqlalchemy import String, DateTime, Integer, Index, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import datetime


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        comment="create time"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
        comment="update time"
    )

class Category(Base):
    __tablename__ = "news_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="category id")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="category name")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="sort order")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"

class News(Base):
    __tablename__ = "news"

    __table_args__ = (
        Index("fk_news_category", "category_id"),  # high frequency visited
        Index("idx_publish_time", "publish_time")  # sorted by time requirement
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="news id")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="news title")
    description: Mapped[Optional[str]] = mapped_column(String(500),comment="news description")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="news content")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="news image url")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="news author")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("news_category.id"), nullable=False, comment="news category id")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="news views")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="news publish time")

    def __repr__(self):
        return f"<News(id={self.id}, title={self.title}, description={self.description}, content={self.content}, image={self.image}, author={self.author}, category_id={self.category_id}, views={self.views}, publish_time={self.publish_time})>"
