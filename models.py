import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
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
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("uuid_generate_v4()"),
    ), sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("sent_at",
                      sqlalchemy.TIMESTAMP,
                      default=datetime.datetime.utcnow),
    sqlalchemy.Column('user_id',
                      UUID(as_uuid=True),
                      sqlalchemy.ForeignKey('users.id'),
                      nullable=False))

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
            await database.execute(str(CreateTable(table)))
        except Exception as e:
            print(e)
    await database.disconnect()
