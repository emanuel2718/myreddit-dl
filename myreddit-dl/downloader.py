import json
import os
import pprint
import praw
import re
import requests
import utils
from item import Item
from datetime import datetime
from defaults import Defaults
from file_handler import FileHandler


class Downloader:
    def __init__(self, client: 'RedditClient') -> None:
        self.client = client
        self.log = utils.setup_logger(__name__, self.client.args['debug'])
        self.valid_domains = self._sfw_domains
        self.download_counter = 0
        self.skipped_counter = 0
        self.items_iterated = 0
        self.item = None
        self.media_url = None
        self.file_handler = None  # will eventually hold current instance of FileHandler
        self._check_metadata_request()

    @property
    def __print_counters(self) -> None:
        self.log.info(f'{self.skipped_counter} media skipped')
        self.log.info(f'{self.download_counter} media downloaded')
        self.log.info(f'{self.items_iterated} posts searched')

    @property
    def user(self) -> str:
        return str(self.client.user)

    @property
    def args(self) -> dict:
        return self.client.args

    @property
    def curr_media_url(self) -> str or list:
        return self.media_url

    def set_media_url(self, url: str) -> None:
        self.media_url = url

    @property
    def _sfw_domains(self) -> set:
        return {'v.redd.it',
                'i.redd.it',
                'i.imgur.com',
                'gfycat.com',
                'streamable.com',
                'reddit.com',
                'imgur.com'}

    @property
    def _nsfw_domains(self) -> set:
        return {'redgifs.com', 'erome.com'}

    @property
    def _is_valid_domain(self) -> bool:
        return True if self.item.get_item().domain in self.valid_domains else False

    @property
    def _is_valid_subreddit(self) -> bool:
        ''' Returns True if any of the asked subreddits with the -sub flag
            matches the current item subreddit.

            Also returns True if the user didn't specify any subreddit, as
            then it is implied that the user wants all the posts.
        '''
        if self.client.args['sub'] is None:
            return True
        return self.subreddit in self.client.args['sub']

    def __debug_item(self):
        return (f'- Link: {self.item.link}\n'
                f'- Domain: {self.item.domain}\n'
                f'- Subreddit: {self.item.subreddit_prefixed}\n'
                f'- Author: {self.item.author}\n')

    def _is_valid_post(self) -> bool:
        # TODO: think about a more clean way to handle this.
        if self.item.get_item() is None:
            return False
        if self.item.author is None:
            return False
        if self.item.item_id is None:
            return False
        if self.is_comment():
            return False
        if not self._is_valid_subreddit:
            return False
        if not self._is_valid_domain:
            return False
        return True

    def is_comment(self) -> bool:
        if isinstance(self.item, praw.models.reddit.comment.Comment):
            return True
        return False

    def get_media_url(self) -> list:
        # TODO: maybe make this into some kind of for loop through
        #       the valid domains?
        if self.item.domain == 'v.redd.it':
            media_url = self.item.get_vreddit_url()
        elif self.item.domain == 'gfycat.com':
            media_url = self.item.get_gyfcat_url()
        elif self.item.domain == 'redgifs.com':
            media_url = self.item.get_redgifs_url()
        elif self.item.domain == 'streamable.com':
            media_url = self.item.get_streamable_url()
        elif self.item.domain == 'imgur.com' and not self.item.url.endswith(('jpg', 'png')):
            media_url = self.item.get_imgur_gallery_url()
        elif self.item.url.startswith(utils.REDDIT_GALLERY_URL):
            media_url = self.item.get_reddit_gallery_url()
        elif self.item.url.endswith('gifv'):
            media_url = self.item.get_mp4_url_from_gif_url()
        else:
            media_url = self.item.url  # all the png and jpg ready for download
        return media_url

    def download_limit_reached(self) -> bool:
        if self.args['limit'] and self.download_counter >= self.args['limit']:
            self.__print_counters
            exit(1)
            return True
        return False

    def __write__(self, url: str, path: str, filename: str):
        try:
            r = requests.get(url)
            with open(path, 'wb') as f:
                f.write(r.content)
                # User didn't specify --no-metadata, go ahead an save metadata
                if not self.client.args['no_metadata']:
                    self.file_handler.save_metadata(path, str(filename))
                    self.log.info(f'ADDED: {filename}')
                self.download_counter += 1
        except BaseException:
            if self.client.args['verbose']:
                self.log.exception(f'While adding file {filename}')

    def download(self):
        data = self.file_handler.absolute_path
        if isinstance(data, list):
            for d in data:
                filename = self.file_handler.get_filename_from_path(d['path'])
                self.__write__(d['url'], d['path'], filename)
        else:
            filename = self.file_handler.get_filename(self.media_url)
            self.__write__(self.media_url, data, filename)

    def can_download_item(self):
        if self.media_url is None:
            return False

        if isinstance(self.media_url, list) and self.client.args['no_gallery']:
            self.log.debug(f'Skipped Gallery Item\n{self.__debug_item()}')
            return False

        filename = self.file_handler.get_filename(self.media_url)

        if self.client.args['only_video'] and not self.file_handler.is_video:
            self.log.bug(f'Skipped Image: {filename}')
            return False

        if self.client.args['no_video'] and self.file_handler.is_video:
            self.log.debug(f'Skipped Video: {filename}')
            return False

        if self.file_handler.file_exist:
            if self.client.args['verbose']:
                self.log.info(f'File exists: {filename}')
            return False

        # NOTE: DONT DO THIS HERE. REFACTOR ME!
        if not os.path.exists(self.file_handler.get_path()):
            self.file_handler.create_path()
        return True

    def _iterate_items(self, items: 'Upvoted or Saved posts') -> None:
        for item in items:
            self.item = Item(item)
            # print(i.__repr__())
            # print(i)
            #self._item = item
            self.items_iterated += 1
            if not self.download_limit_reached() and self._is_valid_post():
                self.media_url = self.get_media_url()
                self.file_handler = FileHandler(self, self.item)
                if self.can_download_item():
                    self.download()
                else:
                    self.skipped_counter += 1
        return self.__print_counters

    def _check_metadata_request(self):
        if self.client.args['delete_database']:
            FileHandler(self).delete_database()
            exit(0)

        options = {
            'get_metadata': None,
            'get_link': 'Link',
            'get_title': 'Title', }
        for opt, val in options.items():
            if self.client.args[opt]:
                FileHandler(self).get_metadata(self.client.args[opt], val)
                exit(0)
                return

    def start(self) -> None:
        if self.client.args['clean_debug']:
            FileHandler(self).clean_debug()

        if self.client.args['nsfw']:
            # union of nsfw and sfw domains
            self.valid_domains |= self._nsfw_domains
        if self.client.args['upvote'] and not self.client.args['saved']:
            self._iterate_items(self.client.upvotes)
        elif self.client.args['saved'] and not self.client.args['upvote']:
            self._iterate_items(self.client.saves)
        elif self.client.args['saved'] and self.client.args['upvote']:
            print('THREADS: iterating both saved and upvotes')
        else:
            utils.print_error(utils.MISSING_DOWNLOAD_SOURCE)


if __name__ == '__main__':
    utils.print_warning(cli.DONT_RUN_THIS_FILE)
