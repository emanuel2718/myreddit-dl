import os


def get_valid_options():
    return {'subreddit',
            'username',
            'subreddit_username',
            'username_subreddit'}


def get_dir_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_new_client(section='NEW_USER'):
    return {'section': section,
            'id': 'new_id',
            'secret': 'new_secret',
            'username': 'new_username',
            'password': 'new_password'}
