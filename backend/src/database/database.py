from typing import Union
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.database.main import Base, InitialMixin

class Database:
    mixin = InitialMixin
    
    engine: Union[AsyncEngine, None] = None
    session: Union[async_sessionmaker, None] = None
    base: Union[DeclarativeBase, None] = None

    def __init__(self, url: Union[str, None] = None) -> None:
        self.base = Base
        
        if url:
            self.init(url)
    
    def init(self, url: str) -> None:
        self.engine = create_async_engine(url, echo=False)
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def init_models(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)
            await conn.run_sync(self.base.metadata.create_all)

    async def get_session(self):
        async with self.session() as session:
            yield session
