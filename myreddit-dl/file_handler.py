import os
import re
import utils
from urllib.parse import urlparse

BASE_PATH = os.getcwd() + os.sep + 'media' + os.sep


class FileHandler():
    def __init__(self, cls):
        self.cls = cls
        self.path = self.get_path()
        self.media_url = self.cls.curr_media_url if self.cls.curr_media_url else ''

    @property
    def filenames_from_list(self):
        count = 0
        filenames = []
        for url in self.media_url:
            filenames.append(self.path + str(count) + self.get_file_extension(url))
            count += 1
        return filenames

    def get_file_extension(self, url):
        parsed = urlparse(url)
        _, ext = os.path.splitext(parsed.path)
        return ext

    def get_filename(self) -> list[str, ...] or str:
        if isinstance(self.media_url, list):
            # TODO: Why is this adding double quotes to the path?
            return self.filenames_from_list
        elif self.media_url.endswith('fallback'):
            return self.path + self.get_file_extension(self.media_url)
        return self.path + self.get_file_extension(self.media_url)

    def get_path(self):
        # TODO: Eventually we want path resolution from path given with --path flag
        return BASE_PATH + str(self.cls.item.author) + '_' + str(self.cls.item.id)


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
