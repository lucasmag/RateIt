def get_user_by_id(user_id):
    return 'select u.username from public.user u where u.id = {}'.format(user_id)


def get_followers_by_user_id(followed_id):
    return 'select f.follower_id from public.follower f where f.followed_id = {}'.format(int(followed_id))


def follow_user(follower_id, followed_id):
    return 'insert into public.follower values ({}, {})'.format(follower_id, followed_id)


def unfollow_user(follower_id, followed_id):
    return 'delete from public.follower f where f.follower_id = {} and f.followed_id = {}'.format(follower_id, followed_id)


def new_user(req):
    return "insert into public.user (username, first_name, last_name, password, email, phone, is_active)" \
           "values ('{}', '{}', '{}', '{}', '{}', '{}', {})".format(req.get('username'), req.get('first_name'),
                                                                    req.get('last_name'), req.get('password'),
                                                                    req.get('email'),
                                                                    req.get('phone'), bool(req.get('is_active')))

