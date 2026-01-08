from fastapi import APIRouter, Depends,Query
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
        "message": "get news list",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }