from sqlalchemy import select, update, func, result_tuple
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_news_list(
        db: AsyncSession,
        category_id: int,
        skip: int = 0,
        limit: int = 10
):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # one result only


async def get_news_details(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # update database: need to check if update is successful.
    return result.rowcount > 0


async def get_related_news(db: AsyncSession, category_id: int, news_id: int, limit: int = 5):
    stmt = select(News).where(
            News.category_id == category_id,
            News.id != news_id
        ).order_by(
            News.views.desc(),
            News.publish_time.desc()
        ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    return [{
        "id": news.id,
        "title": news.title,
        "image": news.image,
        "views": news.views,
        "publishTime": news.publish_time,
        "author": news.author,
        "categoryId": news.category_id,
        "content": news.content
    } for news in related_news]
