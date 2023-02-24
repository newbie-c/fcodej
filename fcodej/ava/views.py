import asyncio
import functools

from starlette.responses import PlainTextResponse, Response
from starlette.exceptions import HTTPException

from ..common.pg import get_conn
from ..errors import E404
from .tools import resize


async def show_avatar(request):
    size = request.path_params['size']
    if size < 22 or size > 160:
        raise HTTPException(status_code=404, detail=E404)
    conn = await get_conn(request.app.config)
    res = await conn.fetchrow(
        'SELECT ava_hash, user_id FROM accounts WHERE ava_hash = $1',
        request.path_params['hash'])
    if res is None:
        raise HTTPException(status_code=404, detail=E404)
    ava = await conn.fetchval(
        'SELECT picture FROM avatars WHERE user_id = $1', res.get('user_id'))
    await conn.close()
    if ava is None:
        loop = asyncio.get_running_loop()
        image = await loop.run_in_executor(
            None, functools.partial(resize, size, None))
        if image:
            response = Response(image, media_type='image/png')
            response.headers.append(
                'cache-control',
                'public, max-age=0')
            return response
    return PlainTextResponse('not implemented yet')
