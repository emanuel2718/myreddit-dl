import cli
import os
import re


def get_path(args, username, sub):
    # by test_dir/subreddit
    if args['debug']:
        return f'{os.getcwd()}{os.sep}test_dir{os.sep}{sub}{os.sep}'

    # by media/subreddit
    if args['subreddit']:
        return f'{os.getcwd()}{os.sep}media{os.sep}{sub}{os.sep}'

    # by media/username
    else:
        return f'{os.getcwd()}{os.sep}media{os.sep}{username}{os.sep}'

def is_media(filename):
    if filename.endswith(('.jpg', '.png', '.jpeg', 'gif', 'gifv')):
        return True
    return False

def get_filename(args, user, item):
    ''' Converts urls of any format like:
            -example: https://i.imgur.com/bMstO8O.jpg
        and extracts only the bMst080.jpg portion of it as the filename.

        If the -user flag was given then append the username before the filename.
            -example: random_bMst080.jpg
    '''
    path = get_path(args, user, item.subreddit)
    if args['user']:
        return path + str(item.author) + '_' + \
            re.search('(?s:.*)\\w/(.*)', item.url).group(1)
    return path + re.search('(?s:.*)\\w/(.*)', item.url).group(1)


if __name__ == '__main__':
    cli.print_warning(cli.DONT_RUN_THIS_FILE)
