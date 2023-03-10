from collections import namedtuple

Perm = namedtuple(
    'Perm',
    ['CANNOT_LOG_IN',
     'READ_JOURNAL',
     'FOLLOW_USERS',
     'LIKE_DISLIKE',
     'SEND_PM',
     'WRITE_COMMENTARY',
     'CREATE_LINK_ALIAS',
     'CREATE_ENTITY',
     'BLOCK_ENTITY',
     'CHANGE_USER_ROLE',
     'UPLOAD_PICTURES',
     'MAKE_ANNOUNCEMENT',
     'ADMINISTER_SERVICE'])

permissions = Perm(
    CANNOT_LOG_IN='заблокирован',
    READ_JOURNAL='читать блоги',
    FOLLOW_USERS='создавать ленту',
    LIKE_DISLIKE='ставить лайки/дизлайки',
    SEND_PM='писать в приват',
    WRITE_COMMENTARY='комментировать блоги',
    CREATE_LINK_ALIAS='создавать алиасы для ссылок',
    CREATE_ENTITY='вести свой блог',
    BLOCK_ENTITY='литовать блоги и комментарии',
    CHANGE_USER_ROLE='назначать разрешения',
    UPLOAD_PICTURES='хранить изображения',
    MAKE_ANNOUNCEMENT='делать объявления',
    ADMINISTER_SERVICE='без ограничений')

Group = namedtuple('Group', ['pariah',
                             'taciturn',
                             'commentator',
                             'blogger',
                             'curator',
                             'keeper',
                             'root'])

groups = Group(pariah='Изгои',
               taciturn='Читатели',
               commentator='Комментаторы',
               blogger='Писатели',
               curator='Модераторы',
               keeper='Хранители',
               root='Администраторы')

initials = {permissions.READ_JOURNAL: True,
            permissions.FOLLOW_USERS: True,
            permissions.LIKE_DISLIKE: True,
            permissions.SEND_PM: True,
            permissions.WRITE_COMMENTARY: True,
            permissions.CREATE_LINK_ALIAS: True,
            permissions.CREATE_ENTITY: True}

roots = [permission for permission in permissions
         if permission != permissions.CANNOT_LOG_IN]


async def get_group(perms):
    if permissions.ADMINISTER_SERVICE in perms:
        return groups.root
    if permissions.CREATE_ENTITY in perms \
            and permissions.UPLOAD_PICTURES in perms \
            and permissions.MAKE_ANNOUNCEMENT in perms \
            and permissions.CHANGE_USER_ROLE in perms:
        return groups.keeper
    if permissions.BLOCK_ENTITY in perms:
        return groups.curator
    if permissions.CREATE_ENTITY in perms \
            or permissions.MAKE_ANNOUNCEMENT in perms \
            or permissions.UPLOAD_PICTURES in perms:
        return groups.blogger
    if permissions.LIKE_DISLIKE in perms \
            or permissions.WRITE_COMMENTARY in perms \
            or permissions.SEND_PM in perms:
        return groups.commentator
    if permissions.READ_JOURNAL in perms:
        return groups.taciturn
    if permissions.CANNOT_LOG_IN in perms:
        return groups.pariah
