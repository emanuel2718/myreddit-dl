import os
import re
import utils
import json
from defaults import Defaults
from urllib.parse import urlparse


class FileHandler():
    def __init__(self, cls: 'Downloader') -> None:
        self.cls = cls
        self.defaults = Defaults(True) if self.cls.args['debug'] else Defaults()
        self.media_url = self.cls.curr_media_url if self.cls.curr_media_url else ''
        self.path = self.defaults.get_base_path()
        self.path = self.path if self.path.endswith('/') else self.path + os.sep
        self.json_file = self.defaults.get_metadata_file(self.cls.user)

    def create_path(self):
        if os.path.isdir(self.path):
            return
        try:
            os.makedirs(self.path)
            utils.print_info(f'Path created: {self.path}')
        except BaseException:
            utils.print_error(f'Invalid path: {self.path}')

    def get_path(self) -> str:
        return self.path

    def get_prefix(self) -> str:
        # TODO: the user will be able to select with --config-save:
        #       1. subreddit_user_id.ext (--config-save subreddit user)
        #       2. subreddit_id.ext (--config-save subreddit)
        #       3. user_subreddit_id.ext (--config-save user subreddit)
        #       4. user_id.ext (--config-save user)
        #       BETTER YET: Ask user to select from a set of options with (1, 2, 3, 4)

        ''' Returns {chosen prefix}_'''
        sub = self.get_subreddit_without_prefix(self.cls.item_subreddit)
        username = str(self.cls.item_author)
        current_set_prefix = self.defaults.get_file_prefix()
        if current_set_prefix == 'username':
            return username + '_'
        elif current_set_prefix == 'subreddit':
            return sub + '_'
        elif current_set_prefix == 'subreddit_username':
            return sub + '_' + username + '_'
        return username + '_' + sub + '_'

    @property
    def gallery_data(self) -> list:
        data = []
        for index, url in enumerate(self.media_url):
            self.cls.set_media_url(url)
            data.append({'url': url, 'path': self.path +
                         self.get_filename(url, str(index))})
        return data

    @property
    def absolute_path(self) -> list or str:
        if isinstance(self.media_url, list):
            return self.gallery_data
        return self.path + self.get_filename(self.media_url)

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
            if os.path.isfile(self.json_file):
                os.remove(self.json_file)
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

        return str(self.get_prefix() + self.cls.item_id + index + extension)

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
        try:
            with open(self.json_file, 'r') as f:
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

        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get_metadata(self, filename, meta_type=None):
        try:
            with open(self.json_file, 'r') as f:
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
