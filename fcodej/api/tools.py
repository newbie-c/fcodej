from ..auth.attri import groups, permissions


async def render_menu(request, data):
    menu = {'cu': bool(data['cu']),
            'priv': permissions.SEND_PM in data['cu']['permissions'],
            'profile': "{0}#profile/{1}".format(
        request.app.url_path_for('index'), data['cu']['username'])}
    data['menu'] = menu


async def check_profile_permissions(cu, user, data):
    data['owner'] = cu['id'] == user['uid']
    data['address'] = cu['id'] == user['uid'] or \
            (permissions.ADMINISTER_SERVICE in cu['permissions']
             or  cu['group'] == groups.keeper or
             (permissions.CHANGE_USER_ROLE in cu['permissions']
              and user['group'] != groups.keeper and
              user['group'] != groups.root))


async def fix_bad_token(config):
    length = config.get('TOKEN_LENGTH')
    return f'Данные устарели, срок действия брелка {length} часов.'


async def define_target_url(request, account, token):
    if account.get('user_id'):
        return f'{request.url_for("index")}#reset-password/{token}'
    return f'{request.url_for("index")}#create-password/{token}'
