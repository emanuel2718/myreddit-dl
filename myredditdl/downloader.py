import time
import requests

import myredditdl.console_args as console_args
import myredditdl.utils as utils
from myredditdl.defaults import Defaults
from myredditdl.file_handler import FileHandler
from myredditdl.item import Item
from myredditdl.reddit_client import RedditClient


class Downloader(RedditClient):
    def __init__(self):
        super().__init__()
        self.args = console_args.get_console_args()
        self.log = utils.setup_logger(__name__, self.args['debug'])
        self.item = None
        self.items_iterated = 0
        self.items_downloaded = 0
        self.items_skipped = 0
        self.valid_domains = None
        self.defaults = Defaults(args['debug'])
        self.file_handler = FileHandler()

    def __str__(self) -> str:
        return (
            '\n---- Results ----\n'
            f'Items Iterated:   {self.items_iterated}\n'
            f'Items Skipped:    {self.items_skipped}\n'
            f'Items Downloaded: {self.items_downloaded}\n'
            f'Total time:       {(time.time() - self.client_time)} seconds\n')

    @property
    def get_args(self):
        ''' Command-line arguments'''
        return self.args

    def get_valid_domains(self) -> set:
        ''' Downloadable domains.
            If the --no-nsfw flag was given the only return SFW domains
            else return a union of both NSFW and SFW domains
        '''
        if self.args['no_nsfw']:
            return self.__sfw_domains()
        return self.__sfw_domains() | self.__nsfw_domains()

    def __sfw_domains(self) -> set:
        return {'v.redd.it',
                'i.redd.it',
                'i.imgur.com',
                'gfycat.com',
                'streamable.com',
                'reddit.com',
                'imgur.com'}

    def __nsfw_domains(self) -> set:
        return {'redgifs.com', 'erome.com'}

    def download_limit_reached(self):
        if self.args['limit'] and self.items_downloaded >= self.args['limit']:
            return True
        return False  # Download limit hasn't been reached or no limit was given

    def is_valid_domain(self) -> bool:
        return self.item.get_domain() in self.valid_domains

    def is_valid_subreddit(self) -> bool:
        return self.args['sub'] is None or self.item.get_subreddit(
        ).lower() in self.args['sub']

    def can_download(self) -> bool:
        if len(self.item) == 0:
            return False
        if len(self.item) > 1 and self.args['no_gallery']:
            return False
        if self.args['only_video'] and not self.item.is_video():
            return False
        if self.args['no_video'] and self.item.is_video():
            return False
        if self.file_handler.file_exists():
            self.log.info('Item exists')
            return False
        return True

    def download_item(self) -> None:
        data = self.get_data()
        for i in range(len(self.item)):
            r = requests.get(data[i].get('url'))
            with open(data[i].get('path'), 'wb') as f:
                f.write(r.content)
                self.log.info(
                    f'Item added: {self.file_handler.get_filename(i)}')

        if not self.args['no_metadata']:
            self.file_handler.save_metadata()

    def get_data(self) -> list:
        return [{'url': self.item.get_media_url()[i],
                 'path': self.file_handler.absolute_path[i]}
                for i in range(len(self.item))]

    def __iterate_items(self, items: 'Upvoted and/or Saved posts') -> None:
        for post_item in items:
            if self.download_limit_reached():
                break
            self.item = Item(post_item)
            self.items_iterated += 1
            if self.is_valid_domain() and self.is_valid_subreddit():
                self.file_handler.set_current_item(self.item)
                if self.can_download():
                    self.download_item()
                    self.items_downloaded += 1
            else:
                self.items_skipped += 1

    def start(self) -> None:
        if not self.build_reddit_instance():
            return

        self.valid_domains = self.get_valid_domains()

        if self.args['upvote']:
            self.__iterate_items(self.client_upvotes)
        elif self.args['saved']:
            self.__iterate_items(self.client_saves)
        else:
            self.log.error(utils.MISSING_DOWNLOAD_SOURCE)

        # TODO: clean folders if --debug flag
        if self.args['debug']:
            self.file_handler.debug_clean()

        self.log.info(self)


if __name__ == '__main__':
    print(utils.DONT_RUN_THIS_FILE)
