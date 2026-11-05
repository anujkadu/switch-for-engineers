from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from efs.config import Settings, get_settings


class Base(DeclarativeBase):
    """Base for EFS-owned models; no domain models are defined in Phase 1."""


class UUIDPrimaryKeyMixin:
    """Marker mixin for future EFS models with UUID primary keys."""


def create_engine_for(settings: Settings | None = None, *, test: bool = False) -> Engine:
    cfg = settings or get_settings()
    url = cfg.test_database_url if test else cfg.database_url
    if not url:
        raise ValueError("EFS_TEST_DATABASE_URL is required for test engine creation")
    return create_engine(url, pool_pre_ping=True, hide_parameters=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@contextmanager
def session_scope(factory: sessionmaker[Session]) -> Iterator[Session]:
    session = factory()
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()
