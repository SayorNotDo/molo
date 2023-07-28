from sanic import Sanic
from sanic.response import text
from api.runner.api import runner
import sqlite3
from sqlalchemy.ext.asyncio import create_async_engine

__name__ = "Molo"
app = Sanic(__name__)
app.blueprint(runner)

bind = create_async_engine("sqlite+aiosqlite:///molo/db/database.db", echo=True)


@app.get("/")
async def hello_world(request):
    return text("Hello world.")


@app.get("/")
async def heart_beat(request):
    return text("ping")


if __name__ == '__main__':
    app.run(debug=True, access_log=True)
