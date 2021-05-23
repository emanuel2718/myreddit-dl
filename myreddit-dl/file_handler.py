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
    def abs_path_list(self) -> list[str, str]:
        count = 0
        filenames = []
        for url in self.media_url:
            filenames.append([url, self.base_path + self.get_filename(url, str(count))])
            count += 1
        return filenames

    @property
    def base_path(self) -> str:
        # TODO: Eventually we want path resolution from path given with --path flag
        if self.cls.args['debug']:
            return (CURRENT_DIR + 'test_dir' + SEP + self.cls.user + SEP
                    + str(self.cls.subreddit) + SEP)
        return BASE_PATH + self.cls.user + SEP + str(self.cls.subreddit) + SEP

    @property
    def absolute_path(self) -> list[str, ...] or str:
        if isinstance(self.media_url, list):
            # TODO: Why is this adding double quotes to the path?
            return self.abs_path_list
            # return self.base_path + self.filenames_from_list
        return self.base_path + self.get_filename(self.media_url)

    def get_filename(self, url: str, index=''):
        return (str(self.cls.item.author) + '_' + self.cls.item.id + index +
                self.get_file_extension(url))

    def get_file_extension(self, url: str):
        parsed = urlparse(url)
        _, ext = os.path.splitext(parsed.path)
        return ext


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
