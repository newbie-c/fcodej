import asyncio

from passlib.hash import pbkdf2_sha256
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from ..auth.attri import permissions
from ..auth.cu import checkcu
from ..common.pg import get_conn
from .redi import assign_cache


class IndexPage(HTTPEndpoint):
    async def get(self, request):
        res = {'cu': None}
        token = request.headers.get('x-auth-token')
        if token:
            res['cu'] = await checkcu(request, token)
            if res.get('cu'):
                res['permissions'] = {name: permission for name, permission
                in zip(permissions._fields, permissions)}
        return JSONResponse(res)


class Captcha(HTTPEndpoint):
    async def get(self, request):
        conn = await get_conn(request.app.config)
        captcha = await conn.fetchrow(
            'SELECT val, suffix FROM captchas ORDER BY random() LIMIT 1');
        res = await assign_cache(
            request.app.rc, 'captcha:',
            captcha.get('suffix'), captcha.get('val'), 180)
        return JSONResponse({'captcha': res,
                             'url': request.url_for(
                                 'captcha:captcha',
                                 suffix=captcha.get('suffix'))})
