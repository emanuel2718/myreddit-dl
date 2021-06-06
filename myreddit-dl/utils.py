import os
from pathlib import Path

# TODO: refactor this entire file.

# Project directory: myreddit-dl/myreddit-dl/
PROJECT_DIR = str(Path(__file__).parent) + os.sep
# Project parent directory: myreddit-dl/
PROJECT_PARENT_DIR = str(Path(__file__).parent.parent) + os.sep

# config file
CFG_FILENAME = PROJECT_DIR + 'config.ini'
CFG_PREFIX_DEFAULT = 'subreddit'


DEVELOPER_APP_INSTRUCTIONS = ('https://github.com/emanuel2718/myreddit-dl'
                              '/blob/master/PRE_INSTALL.md')


INVALID_CFG_OPTION_MESSAGE = ('Invalid save option.\n\n'
                              'Valid Options:\n'
                              '1. --config-prefix username\n'
                              '2. --config-prefix subreddit\n'
                              '3. --config-prefix subreddit username\n'
                              '4. --config-prefix username subreddit\n')



# Domains and usefuls urls
REDDIT_GALLERY_URL = 'https://www.reddit.com/gallery/'
NSFW_DOMAINS = {'redgifs.com', 'erome.com'}
SFW_DOMAINS = {'v.redd.it', 'i.redd.it', 'i.imgur.com',
               'gfycat.com', 'streamable.com', 'reddit.com', 'imgur.com'}

SUPPORTED_MEDIA_FORMATS = ('.jpg', '.png', '.jpeg', '.gif', '.gifv', '.mp4')
EXTENSION_STRING = '.jpg.png.jpeg.gif.gifv.mp4'

# Usefuls messages
DONT_RUN_THIS_FILE = ('This file is not intended to be run by itself. '
                      'See myreddit-dl -h for more information')

USER_NOT_FOUND = 'User not found. Possible error in the `config.ini` file.\n'

MISSING_STORING_METHOD = (
    'Required argument missing.\n\n'
    'Please, Specify storing method.\n\n'
    'Options (--by-user or --by-subreddit): \n\n'
    '--by-subreddit  store media with post subreddit '
    'name in front of filename\n'
    '--by-user\tstore media with post author name in front '
    'of filename\n')

MISSING_DOWNLOAD_SOURCE = ('Required argument missing.\n\n'
                           'Please, specify source of media to download\n\n'
                           'Options (-U and/or -S): \n\n'
                           '-U   download upvoted media\n'
                           '-S   download saved media\n')

def get_valid_prefix_options():
    return ('subreddit', 'username', 'subreddit_username', 'username_subreddit')

#def print_prefix_options():
#    print('Please chose an option: \n')
#    print('\n Filename prefix options:\n')
#    print('1. username_id.ext')
#    print('2. subreddit_id.ext')
#    print('3. username_subreddit_id.ext')
#    print('4. subreddit_username_id.ext')

# MISSING_SEARCH_SOURCE = ('Specify upvoted (-U, --upvote) or saved (-S, --saved) posts. '
# 'See myreddit-dl --help for more information.')


# Helper printing functions
def print_debug(*args) -> None:
    print('\n' + '=' * 70)
    for arg in args:
        print(arg)
    print('=' * 70 + '\n')


def print_done(msg: str) -> None:
    print(f'[DONE] {msg}')


def print_error(msg: str) -> None:
    print(f'[ERROR] {msg}')


def print_failed(msg: str) -> None:
    print(f'[FAILED] {msg}')


def print_file_added_debug(filename: str, path: str) -> None:
    print(f'[ADDED] {filename} at {path}')

def print_file_added(filename: str) -> None:
    print(f'[ADDED] {filename}')

def print_already_exists(filename: str) -> None:
    print(f'[ALREADY EXISTS] {filename}')


def print_file_removed(filename: str) -> None:
    print(f'[DELETE] {filename}')


def print_skipped_image(msg: str) -> None:
    print(f'[SKIPPED IMAGE] {msg}')


def print_skipped_video(msg: str) -> None:
    print(f'[SKIPPED VIDEO] {msg}')


def print_info(msg: str) -> None:
    print(f'[INFO] {msg}')


def print_data(msg: str) -> None:
    print(f'\n{msg}\n')


def print_metadata(data: dict) -> None:
    data = data.replace("{", '').replace("}", '').replace("'", '').split(',')
    print('\n\t[METADATA FOUND]\n')
    for i in data:
        print(i.lstrip(' '))
    print('\n')


def print_editing(msg: str) -> None:
    print(f'[EDIT] {msg}')


def print_ok(msg: str) -> None:
    print(f'[OK] {msg}')


def print_warning(msg: str) -> None:
    print(f'[WARNING] {msg}')


if __name__ == '__main__':
    print_warning(DONT_RUN_THIS_FILE)
