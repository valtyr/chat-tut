import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, dialect
import datetime

# Database table definitions.
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("uuid_generate_v4()"),
    ),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
)

messages = sqlalchemy.Table(
    "messages", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("sent_at",
                      sqlalchemy.DateTime,
                      default=datetime.datetime.utcnow))

tables = [users, messages]


async def set_up():
    import databases
    from sqlalchemy.schema import CreateTable
    from starlette.config import Config

    config = Config('.env')
    DATABASE_URL = config('DATABASE_URL')

    database = databases.Database(DATABASE_URL)

    await database.connect()
    await database.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    for table in tables:
        try:
            await database.execute(
                CreateTable(table.__table__).compile(dialect=dialect()))
        except Exception as e:
            print(e)
    await database.disconnect()