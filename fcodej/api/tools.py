async def define_target_url(request, account, token):
    if account.get('user_id'):
        return request.url_for('reset-password', token=token)
    return request.url_for('create-password', token=token)
