import cli
import os
import re

SUPPORTED_MEDIA_FORMATS = ('.jpg', '.png', '.jpeg', 'gif', 'gifv')

class FileHandler:
    def __init__(self, args, username, item) -> None:
        self.args = args
        self.username = str(username)
        self.sub = str(item.subreddit)
        self.url = str(item.url)
        self.author = str(item.author)
        #self.filename = get_filename()

    def valid_file(self) -> bool:
        if self.file_exists() and not is_media():
            return False
        return True


    def file_exists(self) -> bool:
        ''' File could've been downloaded without using the -user flag (which
            appends the post username in front of the filename) or it could've
            been downloader without the -user flag.

            There are cases where the user has deleted the post and if we try
            to download the post again changing the scheme (-user to no -user flag
            or the reverse) the file will be downloaded again and potentially
            replace the old post with the now deleted (empty) file.

            If the file was downloaded without -user flag and then downloaded using the
            -user flag the filename will change from (the reverse will also be true):

                Example: 2892.png ---> username_2892.png
        '''
        path = self.get_path()
        img_name = re.search('(?s:.*)\\w/(.*)', self.url).group(1)
        file_with_user = path + self.author + '_' + img_name
        file_without_user = path + img_name

        if self.args['user']:
            if os.path.isfile(file_without_user):
                cli.print_editing('')
                os.rename(file_without_user, file_with_user)

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
