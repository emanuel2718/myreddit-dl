import os
import re
import utils
from urllib.parse import urlparse


class FileHandler():
    def __init__(self, cls):
        self.cls = cls

    def get_extension(self, url):
        parsed = urlparse(url)
        _, ext = os.path.splitext(parsed.path)
        return ext

    def get_filename(self) -> list[str, ...] or str:
        media_url = self.cls.curr_media_url if self.cls.curr_media_url else ''
        if isinstance(media_url, list):
            return [str(url + self.get_extension(url)) for url in media_url]
        elif media_url.endswith('fallback'):
            return media_url + '.mp4'
        return media_url




        #url = self.cls.current_media_url
        #if url:
        #    if isinstance(url, list):
        #        # we may need to loop
        #        for i in url:
        #            extension = self.get_extension(i)
        #            print(f'{i} -> {extension}')
        #    else:
        #        if url.endswith('fallback'):
        #            print('Fixed fallback:', url + '.mp4')
        #        else:
        #            print(url)

    #def valid_file(self) -> bool:
    #    if self.file_exists() and not is_media():
    #        return False
    #    return True

    #def file_exists(self) -> bool:
    #    ''' File could've been downloaded without using the -user flag (which
    #        appends the post username in front of the filename) or it could've
    #        been downloader without the -user flag.

    #        There are cases where the user has deleted the post and if we try
    #        to download the post again changing the scheme (-user to no -user flag
    #        or the reverse) the file will be downloaded again and potentially
    #        replace the old post with the now deleted (empty) file.

    #        If the file was downloaded without -user flag and then downloaded using the
    #        -user flag the filename will change from (the reverse will also be true):

    #            Example: 2892.png ---> username_2892.png
    #    '''
    #    path = self.get_path()
    #    img_name = re.search('(?s:.*)\\w/(.*)', self.url).group(1)
    #    file_with_user = path + self.author + '_' + img_name
    #    file_without_user = path + img_name

    #    if self.args['user']:
    #        if os.path.isfile(file_without_user):
    #            utils.print_editing('')
    #            os.rename(file_without_user, file_with_user)

    #def get_path(self) -> str:
    #    # by test_dir/subreddit
    #    if self.args['debug']:
    #        return f'{os.getcwd()}{os.sep}test_dir{os.sep}{self.sub}{os.sep}'

    #    # by media/subreddit
    #    if self.args['subreddit']:
    #        return f'{os.getcwd()}{os.sep}media{os.sep}{self.sub}{os.sep}'

    #    # by media/username
    #    else:
    #        return f'{os.getcwd()}{os.sep}media{os.sep}{self.username}{os.sep}'

    #def is_media(self) -> bool:
    #    if self.get_filename().endswith(utils.SUPPORTED_MEDIA_FORMATS):
    #        return True
    #    return False

    #def get_filename(self) -> str:
    #    ''' Converts urls of any format like:
    #            -example: https://i.imgur.com/bMstO8O.jpg
    #        and extracts only the bMst080.jpg portion of it as the filename.

    #        If the -user flag was given then append the username before the filename.
    #            -example: random_bMst080.jpg
    #    '''
    #    path = self.get_path()
    #    if self.args['user']:
    #        return path + self.author + '_' + \
    #            re.search('(?s:.*)\\w/(.*)', self.url).group(1)
    #    return path + re.search('(?s:.*)\\w/(.*)', self.url).group(1)


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
