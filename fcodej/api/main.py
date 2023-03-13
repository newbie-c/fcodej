import asyncio

from passlib.hash import pbkdf2_sha256
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from ..auth.attri import permissions
from ..auth.cu import checkcu
from ..common.pg import get_conn
from .redi import assign_cache
from .pg import filter_target_user


class Profile(HTTPEndpoint):
    async def get(self, request):
        res = {'user': None}
        username = request.query_params.get('username')
        cu = await checkcu(request, request.headers.get('x-auth-token'))
        if cu is None:
            res['message'] = 'Вы не авторизовались, в доступе отказано.'
            return JSONResponse(res)
        if cu and username:
            conn = await get_conn(request.app.config)
            target = await filter_target_user(request, conn, username)
            await conn.close()
            if target is None:
                res['message'] = f'{username}? Такого пользователя у нас нет.'
                return JSONResponse(res)
            if target and target['uid'] != cu['id'] and \
                    permissions.FOLLOW_USERS not in cu['permissions']:
                res['message'] = 'Для вас доступ закрыт, увы.'
                return JSONResponse(res)
            res['cu'], res['user'] = cu, target
            return JSONResponse(res)
        return JSONResponse(res)


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
