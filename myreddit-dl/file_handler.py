import os
import re
import utils
import json
from urllib.parse import urlparse

DEBUG_PATH = os.getcwd() + os.sep + 'test_dir' + os.sep
DEFAULT_PATH = os.getcwd() + os.sep + 'media' + os.sep
SEP = os.sep


class FileHandler():
    def __init__(self, cls: 'Downloader') -> None:
        self.cls = cls
        self.media_url = self.cls.curr_media_url if self.cls.curr_media_url else ''
        self.path = DEBUG_PATH if self.cls.args['debug'] else DEFAULT_PATH

    @property
    def abs_path_list(self) -> list:
        # TODO: Eventually change this to a dict {'url': url, 'path': path}
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
                return (self.path + self.cls.user + SEP
                        + 'subreddits' + SEP + str(self.cls.subreddit) + SEP)
            else:
                return (self.path + self.cls.user + SEP + self.cls.user + '_all' + SEP)

        if self.cls.args['subreddit']:
            return (self.path + self.cls.user + SEP + 'subreddits'
                    + SEP + str(self.cls.subreddit) + SEP)
        else:
            return self.path + self.cls.user + SEP + self.cls.user + '_all' + SEP

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
                if os.path.exists(path[1]):
                    os.remove(path[1])
                    utils.print_file_removed(path[1])
        else:
            if os.path.exists(self.absolute_path):
                os.remove(self.absolute_path)
                utils.print_file_removed(self.absolute_path)

    @property
    def remove_database(self) -> None:
        # TODO: refactor json file to self.
        try:
            if os.path.isfile(self.path + '.' + self.cls.user + '_links.json'):
                os.remove(self.path + '.' + self.cls.user + '_links.json')
                utils.print_file_removed('Database removed')
        except IOError:
            utils.print_error('Deleting databse.')

    @property
    def is_video(self) -> bool:
        if isinstance(self.media_url, list):
            return True if self.get_filename(self.media_url[0]).endswith('mp4') else False
        return True if self.get_filename(self.media_url).endswith('mp4') else False

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
            utils.print_error(f'Getting the file extension of {url}\n')

    def get_filename_from_path(self, path: str):
        return path.rpartition(os.sep)[-1]

    def update_links(self, path: str, filename: str):
        # TODO: refactor json file to self
        json_file = str(self.path) + '.' + str(self.cls.user) + '_links.json'
        link = 'https://reddit.com' + str(self.cls._item.permalink)
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                if filename not in data:
                    data.update({filename: link})
                    if self.cls.args['verbose']:
                        utils.print_editing(f'Database addition {filename}')
                else:
                    utils.print_info(f'Repeated file: {filename}. Not added')

        except IOError:
            utils.print_info(f'Database created. {filename}')
            data = {f'{filename}': f'{link}'}

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get_link(self, filename):
        json_file = str(self.path) + '.' + str(self.cls.user) + '_links.json'
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                if filename in data:
                    utils.print_link(f'{data[filename]}')
                else:
                    utils.print_error(f'No data found for {filename}')

        except IOError:
            utils.print_error(
                'Database file not found. Must download content first to build database.')


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
