import asyncio

from passlib.hash import pbkdf2_sha256
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from ..auth.attri import permissions
from ..auth.cu import checkcu
from ..common.flashed import set_flashed
from ..common.pg import get_conn
from .pg import filter_user
from .redi import assign_cache, assign_uid, extract_cache
from .tasks import change_pattern, ping_user, rem_old_session
from .tokens import create_login_token


class Login(HTTPEndpoint):
    async def post(self, request):
        d = await request.form()
        login, passwd, rme, cache, captcha, token = (
            d.get('login'), d.get('passwd'),
            int(d.get('rme')), d.get('cache'),
            d.get('captcha'), d.get('token'))
        res = {'token': None}
        if token and await checkcu(token):
            res['message'] = 'Вы уже авторизованы.'
            return JSONResponse(res)
        if not cache:
            await set_flashed(
                request, 'Тест провален, либо устарел, попробуйте снова.')
            return JSONResponse(res)
        suffix, val = await extract_cache(request.app.rc, cache)
        if captcha != val:
            await set_flashed(
                request, 'Тест провален, либо устарел, попробуйте снова.')
            asyncio.ensure_future(
                change_pattern(request.app.config, suffix))
            return JSONResponse(res)
        conn = await get_conn(request.app.config)
        user = await filter_user(conn, login)
        await conn.close()
        if user and pbkdf2_sha256.verify(
                passwd, user.get('password_hash')):
            d = await assign_uid(request.app.rc, 'uid:', rme, user)
            res['token'] = await create_login_token(request, rme, d)
            await set_flashed(request, f'Привет, {user.get("username")}!')
            asyncio.ensure_future(
                ping_user(request.app.config, user.get('id')))
            asyncio.ensure_future(
                change_pattern(request.app.config, suffix))
            if rme:
                asyncio.ensure_future(
                    rem_old_session(
                        request, d, user.get('username')))
                pass
        else:
            await set_flashed(
                request, 'Неверный логин или пароль, вход невозможен.')
            return JSONResponse(res)
        return JSONResponse(res)


class IndexPage(HTTPEndpoint):
    async def get(self, request):
        res = {'cu': await checkcu(
            request, request.query_params.get('token'))}
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
