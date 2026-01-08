from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# placeholder db
ASYNC_DATABASE_URL ="mysql+aiomysql://root:12345678@localhost:3306/news_app?charset=utf8"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()