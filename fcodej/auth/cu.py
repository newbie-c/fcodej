from jwt import PyJWTError, decode


async def checkcu(request, token):
    cache, res = None, None
    if token:
        try:
            cache = decode(
                token,
                request.app.config.get('SECRET_KEY'),
                algorithms=['HS256'])
        except PyJWTError:
            pass
        # to be continued
    return res
