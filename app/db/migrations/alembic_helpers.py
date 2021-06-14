from alembic import op
from sqlalchemy import engine_from_config
from sqlalchemy.engine import reflection


def table_has_column(table, column):
    config = op.get_context().config
    engine = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy."
    )
    insp = reflection.Inspector.from_engine(engine)
    return any(column in col["name"] for col in insp.get_columns(table))
