from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from ..auth.attri import permissions
from ..auth.cu import checkcu


class IndexPage(HTTPEndpoint):
    async def get(self, request):
        res = {'cu': await checkcu(request)}
        if res.get('cu'):
            res['permissions'] = {name: permission for name, permission
                in zip(permissions._fields, permissions)}
        return JSONResponse(res)
