import databases
import uvicorn
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse

config = Config('.env')
DATABASE_URL = config('DATABASE_URL')

# Main application code.
database = databases.Database(DATABASE_URL)
app = Starlette(debug=True)

from models import users


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.route("/users", methods=["GET"])
async def list_notes(request):
    query = users.select()
    results = await database.fetch_all(query)
    content = [{"username": result["username"]} for result in results]
    return JSONResponse(content)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)