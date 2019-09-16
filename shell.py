import databases
from starlette.config import Config

config = Config('.env')
DATABASE_URL = config('DATABASE_URL')

# Main application code.
database = databases.Database(DATABASE_URL)


async def set_up():
    await database.connect()


set_up()

from models import *
