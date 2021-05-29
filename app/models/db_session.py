from pathlib import Path
from typing import Callable, Optional

import sqlalchemy as sa
import sqlalchemy.orm as orm
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core import config
from app.models.modelbase import SqlAlchemyBase

__factory: Optional[Callable[[], Session]] = None
__async_engine: Optional[AsyncEngine] = None


def global_init(db_file: str):
    global __factory, __async_engine

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file.")

    folder = Path(db_file).parent
    folder.mkdir(parents=True, exist_ok=True)

    # Post-recording update:
    # SQLAlchemy started enforcing the underlying Python DB API was truly async
    # We don't really get that with SQLite but when you switch something like Postgres
    # It would "light up" with async. Since recording, SQLAlchemy throws and error
    # if this would be the case. We need to explicitly switch to aiosqlite as below.
    conn_str = "sqlite+pysqlite:///" + db_file.strip()
    async_conn_str = "sqlite+aiosqlite:///" + db_file.strip()
    logger.info("Connecting to DB with {}".format(async_conn_str))
    # print("Connecting to DB with {}".format(async_conn_str))

    # Adding check_same_thread = False after the recording. This can be an issue about
    # creating / owner thread when cleaning up sessions, etc. This is a sqlite restriction
    # that we probably don't care about in this example.
    enable_sql_logging = config.get_settings().ENABLE_SQL_LOGGING
    engine = sa.create_engine(
        conn_str, echo=enable_sql_logging, connect_args={"check_same_thread": False}
    )
    __async_engine = create_async_engine(
        async_conn_str,
        echo=enable_sql_logging,
        connect_args={"check_same_thread": False},
    )
    __factory = orm.sessionmaker(bind=engine)

    import app.models.__all_models  # noqa

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    if not __factory:
        raise Exception("You must call global_init() before using this method.")

    session: Session = __factory()
    session.expire_on_commit = False

    return session


def create_async_session() -> AsyncSession:
    global __async_engine

    if not __async_engine:
        raise Exception("You must call global_init() before using this method.")

    session: AsyncSession = AsyncSession(__async_engine)
    session.sync_session.expire_on_commit = False

    return session


async_session = sessionmaker(
    __async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async_session: AsyncSession = create_async_session()
    async with async_session as session:
        yield session
