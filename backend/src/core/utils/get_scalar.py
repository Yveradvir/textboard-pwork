from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

async def get_scalar(
    db: AsyncSession, 
    query: Type[DeclarativeMeta]
):
    """
    Execute a query and return a single scalar result.

    Parameters:
        db (AsyncSession): The asynchronous database session used to execute the query.
        query (Type[DeclarativeMeta]): The SQLAlchemy query to be executed.

    Returns:
        The scalar result of the query, or None if no result is found.
    """
    return (await db.execute(query)).scalar_one_or_none()
