from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import news
from config.db_conf import get_db

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db=db, skip=skip, limit=limit)

    return {
        "code": 200,
        "message:": "get categories success.",
        "data": categories
    }


@router.get("/list")
async def get_news_list(
        category_id: int = Query(alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db),
):
    # page process -> search new list -> count total number -> compute hasMore
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    has_more = (offset + len(news_list)) < total

    return {
        "code": 200,
        "message": "get news list success.",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }

@router.get("/detail")
async def read_news_detail(
        news_id: int = Query(alias="newsId"),
        db: AsyncSession = Depends(get_db),
):
    news_detail = await news.get_news_details(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="News not found.")

    views_res = await news.increase_news_views(db, news_id)
    if not views_res:
        raise HTTPException(status_code=500, detail="Update views failed.")

    return {
        "code": 200,
        "message": "get news details success.",
        "data": {
            "id": news_id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "category": news_detail.category_id,
            "views": news_detail.views,
            "publishTime": news_detail.publish_time,
        }
    }