import os
import logging
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

VIDEO_DOMAINS = {'redgifs.com', 'gfycat.com', 'v.redd.it'}

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
    return (
        'subreddit',
        'username',
        'subreddit_username',
        'username_subreddit')

# def print_prefix_options():
#    print('Please chose an option: \n')
#    print('\n Filename prefix options:\n')
#    print('1. username_id.ext')
#    print('2. subreddit_id.ext')
#    print('3. username_subreddit_id.ext')
#    print('4. subreddit_username_id.ext')

# MISSING_SEARCH_SOURCE = ('Specify upvoted (-U, --upvote) or saved (-S, --saved) posts. '
# 'See myreddit-dl --help for more information.')


def print_metadata(data: dict) -> None:
    data = data.replace("{", '').replace("}", '').replace("'", '').split(',')
    print('\n\t[METADATA FOUND]\n')
    for i in data:
        print(i.lstrip(' '))
    print('\n')



def setup_logger(module: str, debug=False):
    logger = logging.getLogger(module)
    #logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('debug_log', 'a')
    #fh = logging.FileHandler('debug_log', 'w')
    fh.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)


    fh_formatter = logging.Formatter('%(levelname)s: %(name)s : %(message)s')
    sh_formatter = logging.Formatter('%(levelname)s: %(message)s')
    fh.setFormatter(fh_formatter)
    sh.setFormatter(sh_formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)
    logging.getLogger('praw').setLevel(logging.CRITICAL)

    if module == 'reddit_client':
        logger.debug('-'*60)
    return logger


if __name__ == '__main__':
    print_warning(DONT_RUN_THIS_FILE)
