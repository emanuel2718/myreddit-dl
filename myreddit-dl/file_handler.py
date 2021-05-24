import os
import re
import utils
from urllib.parse import urlparse

BASE_PATH = os.getcwd() + os.sep + 'media' + os.sep
CURRENT_DIR = os.getcwd() + os.sep
SEP = os.sep


class FileHandler():
    def __init__(self, cls: 'Downloader') -> None:
        self.cls = cls
        self.media_url = self.cls.curr_media_url if self.cls.curr_media_url else ''

    @property
    def abs_path_list(self) -> list:
        count = 0
        filenames = []
        for url in self.media_url:
            self.cls.set_media_url(url)
            filenames.append([url, self.base_path + self.get_filename(url, str(count))])
            count += 1
        return filenames

    @property
    def base_path(self) -> str:
        # TODO: This is messy. Clean this!
        # TODO: Eventually we want path resolution from path given with --path flag
        if self.cls.args['debug']:
            if self.cls.args['subreddit']:
                return (CURRENT_DIR + 'test_dir' + SEP + self.cls.user + SEP
                        + 'subreddits' + SEP + str(self.cls.subreddit) + SEP)
            else:
                return (CURRENT_DIR + 'test_dir' + SEP + self.cls.user + SEP
                        + self.cls.user + '_all' + SEP)
        if self.cls.args['subreddit']:
            return (BASE_PATH + self.cls.user + SEP + 'subreddits'
                    + SEP + str(self.cls.subreddit) + SEP)
        else:
            return BASE_PATH + self.cls.user + SEP + self.cls.user + '_all' + SEP

    @property
    def absolute_path(self) -> list:
        if isinstance(self.media_url, list):
            return self.abs_path_list
        return self.base_path + self.get_filename(self.media_url)

    @property
    def file_exist(self) -> bool:
        if isinstance(self.absolute_path, list):
            # If the first path exists then all the other media
            # in the gallery is also prenent.
            # list of the type: [path, ..]
            try:
                if os.path.isfile(self.absolute_path[0]):
                    return True
            except BaseException:
                pass

            # list of the type: [[url, path], ...]
            try:
                if os.path.isfile(self.absolute_path[0][1]):
                    return True
            except BaseException:
                utils.print_error('File not found: {self.absolute_path}')
                return False

        elif os.path.isfile(self.absolute_path):
            return True
        return False

    @property
    def remove_file(self) -> None:
        if isinstance(self.absolute_path, list):
            for path in self.absolute_path:
                if os.path.exists(path):
                    os.remove(path)
                    utils.print_file_removed(path)
        else:
            if os.path.exists(self.absolute_path):
                os.remove(self.absolute_path)
                utils.print_file_removed(self.absolute_path)



    def get_filename(self, url: str, index='') -> str:
        extension = self.get_file_extension(url)
        if extension in ['.gif', '.gifv']:
            return (str(self.cls.item.author) + '_' + str(self.cls.item.id) + index +
                    '.mp4')
        return (str(self.cls.item.author) + '_' + str(self.cls.item.id) + index +
                str(self.get_file_extension(url)))

    def get_file_extension(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            _, ext = os.path.splitext(parsed.path)
            return ext
        except BaseException:
            utils.print_error(url)


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
