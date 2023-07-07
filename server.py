from sanic import Sanic
from sanic.response import text
from api.runner.api import runner

__name__ = "Molo"
app = Sanic(__name__)
app.blueprint(runner)


@app.get("/")
async def hello_world(request):
    return text("Hello world.")
