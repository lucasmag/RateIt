def get_users():
    return 'select u.username from public.user u;'


def get_user_by_id(id):
    return 'select u.username from public.user u where u.id = %d' % int(id)


def get_followers_by_user_id(id):
    return 'select f.follower_id from public.follower f where f.user_id = %d' % int(id)


def rate_movie(user_id, movie_id, rating):
    return 'insert into public.watched_movies (user_id, movie_id, favorite, rate) values ({}, {}, false, {})'.format(user_id, movie_id, rating)


def sync_movie(movie_id):
    return 'select m.vote_count, m.vote_average from public.movie m where m.movie_id = {}'.format(movie_id)


def get_movie_by_id(movie_id):
    return 'select * from public.movie m where m.movie_id = {}'.format(movie_id)


def new_movie(movie_id):
    return 'insert into public.movie values ({}, 0, 0, 0)'.format(movie_id)
