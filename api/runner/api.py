from sanic.response import json
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.log import logger
import aiohttp


runner = Blueprint("runner_bp", url_prefix="/runner", version=1)


@runner.route("/")
async def bp_root(request):
    return json({"Hello": "Runner"})


class UiTestView(HTTPMethodView):
    async def post(self, request):
        # 1.基于请求向云端拉取测试用例集合文件（.json）
        url = ""
        payload = {}
        async with runner.post(url, json=payload) as response:
            response_data = await response.json()
            print(response_data)
        # 2.下载文件至本地存储（校验用例集合是否已经下载）(用例文件一般不超过5MB)
        # 3.传入测试框架驱动（异步执行）
        # 4.响应接口
        body = request.json
        if body is not None:
            logger.info("body: ", body)
        return json({"run": "ui-test"})


runner.add_route(UiTestView.as_view(), "/ui-test")
