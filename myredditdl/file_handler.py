import json
import os
import re
from urllib.parse import urlparse
import myredditdl.utils as utils
from myredditdl.console_args import get_console_args as args
from myredditdl.defaults import Defaults


class FileHandler:
    def __init__(self):
        self.log = utils.setup_logger(__name__, args()['debug'])
        self.item = None
        self.defaults = Defaults()

    @property
    def media_path(self) -> str:
        return self.defaults.media_path

    @property
    def absolute_path(self) -> list:
        return [self.media_path + self._filename(url, str(i))
                for i, url in enumerate(self.item.get_media_url())]

    def set_current_item(self, item: 'Reddit post item'):
        self.item = item

    def file_exists(self):
        if os.path.isfile(self.absolute_path[0]):
            return True
        else:
            self.create_path()
            return False

    def create_path(self):
        if os.path.isdir(self.media_path):
            return
        try:
            os.makedirs(self.media_path)
            self.log.info(f'Path created: {self.media_path}')
        except Exception:
            self.log.bebug(f'invalid path: {self.media_path}')

    def _filename(self, url: str, index='') -> str:
        extension = self.get_extension(url)
        prefix = self.defaults.current_prefix
        index = '' if index == '0' else index
        return self.prefix_map().get(prefix) + self.item.get_id() + index + extension

    def get_extension(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            _, ext = os.path.splitext(parsed.path)

        except Exception:
            self.log.error(f'Getting file extension of {url}')

        return ext if not ext.endswith('.gifv') else '.mp4'

    def prefix_map(self) -> dict:
        username = self.item.get_author()
        subreddit = self.item.get_subreddit()
        return {'username': username + '_',
                'subreddit': subreddit + '_',
                'subreddit_username': subreddit + '_' + username + '_',
                'username_subreddit': username + '_' + subreddit + '_',
                }

    def get_filename(self, index: int) -> str:
        _, filename = os.path.split(self.absolute_path[index])
        return filename

    def _get_item_metadata(self) -> dict:
        return {'Author': self.item.get_author(),
                'Subreddit': self.item.get_subreddit_prefixed(),
                'Title': self.item.get_title(),
                'Link': self.item.get_reddit_link(),
                'Upvotes': self.item.get_upvotes_amount(),
                'NSFW': self.item.is_nsfw(),
                'Post creation date': self.item.get_creation_date()
                }


        #
        #    def delete_database(self) -> None:
        #        try:
        #            if os.path.isfile(self.json_file):
        #                os.remove(self.json_file)
        #                self.log.debug('Database deleted')
        #        except IOError:
        #            self.log.error('While deleting database')
        #
        #
        #    def get_filename_from_path(self, path: str):
        #        return path.rpartition(os.sep)[-1]
        #
        #
        #    def save_metadata(self, path: str, filename: str):
        #        try:
        #            with open(self.json_file, 'r') as f:
        #                data = json.load(f)
        #                if filename not in data:
        #                    data[filename] = self._get_item_metadata()
        #                    if self.cls.args['verbose']:
        #                        self.log.debug(f'Added to database: {filename}')
        #                else:
        #                    self.log.debug(f'Already in database: {filename}')
        #
        #        except IOError:
        #            self.log.debug(f'Database created for {self.cls.user}')
        #            data = {f'{filename}': self._get_item_metadata()}
        #
        #        with open(self.json_file, 'w') as f:
        #            json.dump(data, f, indent=4)
        #
        #    def get_metadata(self, filename, meta_type=None):
        #        try:
        #            with open(self.json_file, 'r') as f:
        #                data = json.load(f)
        #                if filename in data.keys():
        #                    if meta_type:
        #                        utils.print_data(
        #                            f'[{meta_type.upper()}] {data[filename][meta_type]}')
        #                    else:
        #                        utils.print_metadata(f'{data[filename]}')
        #                else:
        #                    self.log.error(f'No data found for {filename}')
        #
        #        except IOError:
        #            self.log.error('Database not found. Must download content first')
        #
        #    def clean_debug(self):
        #        try:
        #            os.removedirs(self.defaults.debug_path)
        #            self.log.info('debug_media/ removed')
        #
        #        except:
        #            self.log.info('No debug_media folder to delete')
        #
        #        try:
        #            os.remove(self.defaults.debug_log_file)
        #            self.log.info('debug_log file removed')
        #
        #        except:
        #            self.log.info('No debug_log file found')
        #        exit(0)

if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
