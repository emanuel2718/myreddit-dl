import os
import json
import shutil
from urllib.parse import urlparse
import myredditdl.utils as utils
from myredditdl.defaults import Defaults


class FileHandler:
    def __init__(self):
        self.log = utils.setup_logger(__name__, True)
        self.item = None
        self.defaults = Defaults()

    @property
    def media_path(self) -> str:
        return self.defaults.media_path

    @property
    def absolute_path(self) -> list:
        return [self.media_path + self._filename(url, str(i))
                for i, url in enumerate(self.item.get_media_url())]

    def _filename(self, url: str, index='') -> str:
        extension = self.get_extension(url)
        prefix = self.defaults.current_prefix
        index = '' if index == '0' else index
        return self.prefix_map().get(prefix) + self.item.get_id() + index + extension

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

    def save_metadata(self) -> None:
        filename = self.get_filename(0)
        try:
            with open(self.defaults.metadata_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if filename not in data:
                    data[filename] = self.item.get_metadata()
                    self.log.debug(f'Metadata addition: {filename}')
                else:
                    self.log.debug(f'Metadata exists: {filename}')

        except Exception:
            self.log.debug(
                f'Metadata file created: {self.defaults.metadata_file}')
            data = {f'{filename}': self.item.get_metadata()}

        with open(self.defaults.metadata_file, 'w') as f:
            json.dump(data, f, indent=4)

    def debug_clean(self) -> None:
        try:
            shutil.rmtree(self.defaults.debug_media_dir)
            self.log.debug('Debug media folder removed')

        except FileNotFoundError:
            self.log.debug('No debug media folder found')

        try:
            os.remove(self.defaults.metadata_file)
            self.log.debug(
                f'Metadata file removed: {self.defaults.metadata_file}')

        except FileNotFoundError:
            self.log.debug('No debug metadata file found')


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
