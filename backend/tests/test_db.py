from efs.config import Settings
from efs.db import create_engine_for
from sqlalchemy.engine import make_url


def test_engine_configuration():
    engine = create_engine_for(Settings(database_url="postgresql+psycopg://u:p@h/db"))
    assert make_url(str(engine.url)).drivername == "postgresql+psycopg"
    assert engine.pool._pre_ping is True
    engine.dispose()
