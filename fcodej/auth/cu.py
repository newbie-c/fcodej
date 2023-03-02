import asyncio

from jwt import PyJWTError, decode

from ..api.tasks import ping_user
from ..api.tokens import check_token
from ..auth.attri import get_group, permissions


async def checkcu(request, token):
    cache = await check_token(request.app.config, token)
    if cache:
        uid = await request.app.rc.get(cache.get('cache')) or '0'
        query = await request.app.rc.hgetall(f'data:{uid}')
        if query:
            if permissions.CANNOT_LOG_IN in query.get('permissions'):
                print('whoops!')
                await request.app.rc.delete(cache.get('cache'))
                await request.app.rc.delete(f'data:{uid}')
                return None
            asyncio.ensure_future(
                ping_user(request.app.config, int(uid)))
            return {'id': int(query.get('id')),
                    'username': query.get('username'),
                    'group': await get_group(query.get('permissions')),
                    'registered': query.get('registered'),
                    'permissions': query.get('permissions').split(','),
                    'ava': request.url_for(
                        'ava:avatar', hash=query.get('ava'), size=22)}
    return None
