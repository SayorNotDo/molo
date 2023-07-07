from sanic.response import json
from sanic import Blueprint

runner = Blueprint("runner_bp", url_prefix="/runner", version=1)


@runner.route("/")
async def bp_root(request):
    return json({"Hello": "Runner"})
