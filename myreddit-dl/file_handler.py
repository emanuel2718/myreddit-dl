import cli
import os
import re

SUPPORTED_MEDIA_FORMATS = ('.jpg', '.png', '.jpeg', 'gif', 'gifv')

class FileHandler:
    def __init__(self, args, username, item) -> None:
        self.args = args
        self.username = username
        self.sub = item.subreddit
        self.url = item.url
        self.author = item.author

    def get_path(self) -> str:
        # by test_dir/subreddit
        if self.args['debug']:
            return f'{os.getcwd()}{os.sep}test_dir{os.sep}{self.sub}{os.sep}'

        # by media/subreddit
        if self.args['subreddit']:
            return f'{os.getcwd()}{os.sep}media{os.sep}{self.sub}{os.sep}'

        # by media/username
        else:
            return f'{os.getcwd()}{os.sep}media{os.sep}{self.username}{os.sep}'

    def is_media(self) -> bool:
        if self.get_filename().endswith(SUPPORTED_MEDIA_FORMATS):
            return True
        return False

    def get_filename(self) -> str:
        ''' Converts urls of any format like:
                -example: https://i.imgur.com/bMstO8O.jpg
            and extracts only the bMst080.jpg portion of it as the filename.

            If the -user flag was given then append the username before the filename.
                -example: random_bMst080.jpg
        '''
        path = self.get_path()
        if self.args['user']:
            return path + self.author + '_' + \
                re.search('(?s:.*)\\w/(.*)', self.url).group(1)
        return path + re.search('(?s:.*)\\w/(.*)', self.url).group(1)


if __name__ == '__main__':
    cli.print_warning(cli.DONT_RUN_THIS_FILE)
