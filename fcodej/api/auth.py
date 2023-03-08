import asyncio

from passlib.hash import pbkdf2_sha256
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from ..auth.cu import checkcu
from ..common.flashed import set_flashed
from ..common.pg import get_conn
from .pg import check_address, filter_user
from .redi import assign_uid, extract_cache
from .tasks import change_pattern, rem_old_session, request_password
from .tokens import check_token, create_login_token


class CreatePassword(HTTPEndpoint):
    async def get(self, request):
        res = {'cu': None, 'aid': None}
        auth = request.headers.get('x-auth-token')
        cu = await checkcu(request, auth)
        token = request.headers.get('x-reg-token')
        if cu:
            res['cu'] = cu
            res['message'] = '''Вы авторизованы, действие невозможно,
            нужно выйти и повторить переход по ссылке.'''
            return JSONResponse(res)
        acc = await check_token(request.app.config, token)
        if acc is None:
            length = request.app.config.get('TOKEN_LENGTH')
            mes = f'Данные устарели, срок действия брелка {length} часов.'
            res['message'] = mes
            return JSONResponse(res)
        conn = await get_conn(request.app.config)
        acc = await conn.fetchrow(
            'SELECT id, address, user_id FROM accounts WHERE id = $1',
            acc.get('aid'))
        await conn.close()
        if acc.get('user_id'):
            res['message'] = 'Пользователь на этом аккаунте уже создан.'
            return JSONResponse(res)
        res['aid'] = acc.get('id')
        return JSONResponse(res)

    async def post(self, request):
        return JSONResponse({'result': 'empty'})


class GetPassword(HTTPEndpoint):
    async def post(self, request):
        d = await request.form()
        address, cache, captcha, token = (
            d.get('address'), d.get('cache'),
            d.get('captcha'), d.get('token'))
        res = {'result': 'empty'}
        if token and await checkcu(token):
            await set_flashed(request, 'Вы авторизованы.')
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
        message, account = await check_address(request, conn, address)
        await conn.close()
        if message:
            await set_flashed(request, message)
            asyncio.ensure_future(
                change_pattern(request.app.config, suffix))
            return JSONResponse(res)
        asyncio.ensure_future(
            change_pattern(request.app.config, suffix))
        asyncio.ensure_future(
            request_password(request, account, address))
        await set_flashed(
            request, 'На ваш адрес выслано письмо с инструкциями.')
        return JSONResponse(res)


class Login(HTTPEndpoint):
    async def post(self, request):
        d = await request.form()
        login, passwd, rme, cache, captcha, token = (
            d.get('login'), d.get('passwd'),
            int(d.get('rme')), d.get('cache'),
            d.get('captcha'), d.get('token'))
        res = {'token': None}
        if token and await checkcu(token):
            await set_flashed(request, 'Вы уже авторизованы.')
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
                change_pattern(request.app.config, suffix))
            if rme:
                asyncio.ensure_future(
                    rem_old_session(
                        request, d, user.get('username')))
        else:
            await set_flashed(
                request, 'Неверный логин или пароль, вход невозможен.')
            return JSONResponse(res)
        return JSONResponse(res)


class Logout(HTTPEndpoint):
    async def post(self, request):
        res = {'result': None}
        token = (await request.form()).get('token')
        if token:
            cache = await check_token(request.app.config, token)
            if cache:
                uid = await request.app.rc.get(cache.get('cache'))
                cu = await checkcu(request, token)
                if cu.get('id') == int(uid):
                    await request.app.rc.delete(cache.get('cache'))
                    res['result'] = True
                    await set_flashed(request, f'Пока, {cu.get("username")}!')
        return JSONResponse(res)

