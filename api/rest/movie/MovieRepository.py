def get_users():
    return 'select u.username from public.user u;'


def get_user_by_id(id):
    return 'select u.username from public.user u where u.id = %d' % int(id)


def get_followers_by_user_id(id):
    return 'select f.follower_id from public.follower f where f.user_id = %d' % int(id)


