import os
import re
import utils
import json
from defaults import Defaults
from urllib.parse import urlparse

# TODO: refactor this
DEBUG_PATH = os.getcwd() + os.sep + 'test_media' + os.sep
DEFAULT_PATH = os.getcwd() + os.sep + 'media' + os.sep
SEP = os.sep


class FileHandler():
    def __init__(self, cls: 'Downloader') -> None:
        self.cls = cls
        self.defaults = Defaults(self.cls.args)
        self.media_url = self.cls.curr_media_url if self.cls.curr_media_url else ''
        self.path = DEBUG_PATH if self.cls.args['debug'] else DEFAULT_PATH

    @property
    def gallery_data(self) -> list:
        data = []
        for index, url in enumerate(self.media_url):
            self.cls.set_media_url(url)
            data.append({'url': url, 'path': self.base_path +
                         self.get_filename(url, str(index))})
        return data

    @property
    def base_path(self) -> str:
        return self.path + self.cls.user + SEP

    @property
    def absolute_path(self) -> list or str:
        if isinstance(self.media_url, list):
            return self.gallery_data
        return self.base_path + self.get_filename(self.media_url)

    @property
    def file_exist(self) -> bool:
        if isinstance(self.absolute_path, list):
            try:
                if os.path.isfile(self.absolute_path[0]['path']):
                    return True
            except BaseException:
                utils.print_error(
                    f'File not found: {self.absolute_path[0]["path"]}')
                return False

        elif os.path.isfile(self.absolute_path):
            return True
        return False

    @property
    def remove_file(self) -> None:
        if isinstance(self.absolute_path, list):
            for data in self.gallery_data:
                if os.path.exists(data['path']):
                    os.remove(data['path'])
                    utils.print_file_removed(data['path'])
        else:
            if os.path.exists(self.absolute_path):
                os.remove(self.absolute_path)
                utils.print_file_removed(self.absolute_path)

    @property
    def delete_database(self) -> None:
        try:
            # TODO: REFACTOR ME!
            # TODO: change user_links.json ----> user_metadata.json
            if os.path.isfile(self.path + self.cls.user + '_metadata.json'):
                os.remove(self.path + self.cls.user + '_metadata.json')
                utils.print_file_removed('Database deleted')
        except IOError:
            utils.print_error('While deleting databse.')

    @property
    def is_video(self) -> bool:
        if isinstance(self.media_url, list):
            return True if self.get_filename(
                self.media_url[0]).endswith('mp4') else False
        return True if self.get_filename(
            self.media_url).endswith('mp4') else False

    def get_filename(self, url: str, index='') -> str:
        url = url[0] if isinstance(url, list) else url
        extension = str(self.get_file_extension(url))

        #if self.cls.args['by_user']:
        return str(self.cls.item_author + '_' + self.cls.item_id
                    + index + extension)

        #sub = self.get_subreddit_without_prefix(self.cls.item_subreddit)
        #return str(sub + '_' + self.cls.item_author + '_' + self.cls.item_id
        #           + index + extension)

    def get_subreddit_without_prefix(self, sub: str) -> str:
        ''' Receive a r/subreddit string and return subreddit without
            the r/ prefix
        '''
        return sub.split('/')[1]

    def get_file_extension(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            _, ext = os.path.splitext(parsed.path)
            return ext if not ext.endswith('.gifv') else '.mp4'
        except BaseException:
            utils.print_error(f'Getting the file extension of {url}\n')

    def get_filename_from_path(self, path: str):
        return path.rpartition(os.sep)[-1]

    def _get_item_metadata(self) -> dict:
        return {'Author': self.cls.item_author,
                'Subreddit': self.cls.item_subreddit,
                'Title': self.cls.item_title,
                'Link': self.cls.item_link,
                'Upvotes': self.cls.item_upvotes,
                'NSFW': self.cls.item_nsfw,
                'Post creation date': self.cls.item_creation_date
                }

    def save_metadata(self, path: str, filename: str):
        json_file = str(self.path) + str(self.cls.user) + '_metadata.json'
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                if filename not in data:
                    data[filename] = self._get_item_metadata()
                    if self.cls.args['verbose']:
                        utils.print_editing(f'Database addition {filename}')
                else:
                    utils.print_info(f'Repeated file: {filename}. Not added')

        except IOError:
            utils.print_info(f'Database created for {self.cls.user}')
            data = {f'{filename}': self._get_item_metadata()}

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get_metadata(self, filename, meta_type=None):
        json_file = str(self.path) + str(self.cls.user) + '_metadata.json'
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                if filename in data.keys():
                    if meta_type:
                        utils.print_data(
                            f'[{meta_type.upper()}] {data[filename][meta_type]}')
                    else:
                        utils.print_metadata(f'{data[filename]}')
                else:
                    utils.print_error(f'No data found for {filename}')

        except IOError:
            utils.print_error(
                'Database file not found. Must download content first to build database.')


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
