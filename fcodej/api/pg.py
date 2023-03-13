from datetime import datetime, timedelta
from hashlib import md5

from validate_email import validate_email

from ..auth.attri import get_group, permissions


async def filter_target_user(request, conn, username):
    query = await conn.fetchrow(
        '''SELECT users.id AS uid,
                  users.username AS username,
                  users.registered AS registered,
                  users.last_visit AS last_visit,
                  users.permissions AS permissions,
                  users.description AS description,
                  users.last_published AS last_pub,
                  accounts.address AS address,
                  accounts.ava_hash AS ava_hash
             FROM users, accounts WHERE users.username = $1
               AND users.id = accounts.user_id''',
        username)
    if query:
        return {'uid': query.get('uid'),
                'username': query.get('username'),
                'group': await get_group(query.get('permissions')),
                'registered': f'{query.get("registered").isoformat()}Z',
                'last_visit': f'{query.get("last_visit").isoformat()}Z',
                'permissions': query.get('permissions'),
                'description': query.get('description'),
                'last_pub': f'{query.get("last_pub").isoformat()}Z'
                if query.get('last_pub') else None,
                'address': query.get('address'),
                'ava': request.url_for(
                    'ava:avatar', hash=query.get('ava_hash'), size=160)}


async def define_a(conn, account):
    if account and account.get('user_id'):
        username = await conn.fetchval(
            'SELECT username FROM users WHERE id = $1', account.get('user_id'))
        return username, 'Сброс забытого пароля', 'emails/resetpwd.html'
    return 'Гость', 'Регистрация', 'emails/invitation.html'


async def get_acc(conn, account, address):
    now = datetime.utcnow()
    if account:
        address = account.get('address')
        await conn.execute(
            '''UPDATE accounts SET swap = null, requested = $1
                 WHERE address = $2''', now, address)
    else:
        await conn.execute(
            '''INSERT INTO accounts (address, ava_hash, requested)
                 VALUES ($1, $2, $3)''',
            address, md5(address.encode('utf-8')).hexdigest(), now)
    return await conn.fetchrow(
        'SELECT id, address, user_id FROM accounts WHERE address = $1',
        address)


async def check_swap(conn, address, length):
    swapped = await conn.fetchrow(
        'SELECT id, swap, requested FROM accounts WHERE swap = $1', address)
    if swapped:
        if datetime.utcnow() - swapped.get('requested') > length:
            await conn.execute(
                'UPDATE accounts SET swap = null WHERE id = $1',
                swapped.get('id'))
            return None
        else:
            return True


async def check_address(request, conn, address):
    message = None
    interval = timedelta(
        seconds = round(
            3600*request.app.config.get('REQUEST_INTERVAL', cast=float)))
    length = timedelta(
        seconds = round(
            3600*request.app.config.get('TOKEN_LENGTH', cast=float)))
    acc = await conn.fetchrow(
        'SELECT address, requested, user_id FROM accounts WHERE address = $1',
        address)
    if acc and datetime.utcnow() - acc.get('requested') < interval:
        message = 'Сервис временно недоступен, попробуйте зайти позже.'
    if await check_swap(conn, address, length):
        message = 'Адрес в свопе, выберите другой или повторите попытку позже.'
    return message, acc


async def filter_user(conn, login):
    squery = '''SELECT users.id AS id,
                       users.username AS username,
                       users.password_hash AS password_hash,
                       users.permissions AS permissions,
                       users.registered AS registered,
                       accounts.ava_hash AS ava
                  FROM users, accounts WHERE users.id = accounts.user_id'''
    if validate_email(login):
        squery += ' AND accounts.address = $1'
    else:
        squery += ' AND users.username = $1'
    query = await conn.fetchrow(squery, login)
    if query and permissions.CANNOT_LOG_IN not in query.get('permissions'):
        return {'id': query.get('id'),
                'username': query.get('username'),
                'password_hash': query.get('password_hash'),
                'registered': query.get('registered'),
                'permissions': query.get('permissions'),
                'ava': query.get('ava')}
