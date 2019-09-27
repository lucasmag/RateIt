def get_users():
    return 'select u.username from public.user u;'


def get_user_by_id(id):
    return 'select u.username from public.user u where u.id = %d' % int(id)

