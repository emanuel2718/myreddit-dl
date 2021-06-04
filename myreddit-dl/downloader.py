import json
import os
import pprint
import praw
import re
import requests
import utils
from datetime import datetime
from defaults import Defaults
from file_handler import FileHandler


class Downloader:
    def __init__(self, client: 'RedditClient') -> None:
        self.client = client
        self.valid_domains = utils.SFW_DOMAINS
        self.download_counter = 0
        self.items_iterated = 0

        self._item = None  # current upvoted or saved post we are looking at.
        self.media_url = None
        self.file_handler = None  # will eventually hold current instance of FileHandler
        self._check_metadata_request()
        self.start()

    @property
    def __print_item(self) -> None:
        pprint.pprint(vars(self._item))

    @property
    def __print_counters(self) -> None:
        if self.client.args['debug'] or self.client.args['verbose']:
            utils.print_info(f'{self.download_counter} items downloaded.')
            utils.print_info(f'{self.items_iterated} posts iterated.')

    @property
    def item(self) -> 'RedditPostItem':
        return self._item

    @property
    def item_id(self) -> str:
        return self._item.id

    @property
    def item_link(self) -> str:
        return str('https://reddit.com' + self._item.permalink)

    @property
    def item_title(self) -> str:
        return str(self._item.title)

    @property
    def item_subreddit(self) -> str:
        return str(self._item.subreddit_name_prefixed)

    @property
    def item_upvotes(self) -> int:
        return self._item.ups

    @property
    def item_author(self) -> str:
        return str(self._item.author)

    @property
    def item_nsfw(self) -> bool:
        return self._item.over_18

    @property
    def item_creation_date(self) -> str:
        time_utc = self._item.created_utc
        return str(datetime.fromtimestamp(time_utc).strftime('%m/%d/%Y'))

    @property
    def user(self) -> str:
        return str(self.client.user)

    @property
    def args(self) -> dict:
        return self.client.args

    @property
    def subreddit(self) -> str:
        return str(self._item.subreddit)

    @property
    def curr_media_url(self) -> str or list:
        return self.media_url

    def set_media_url(self, url: str) -> None:
        self.media_url = url

    @property
    def sfw_domains(self) -> set:
        return utils.SFW_DOMAINS

    @property
    def nsfw_domains(self) -> set:
        return utils.NSFW_DOMAINS

    @property
    def _vreddit_url(self) -> str:
        ''' For the https://v.redd.it posts'''
        if self._item.media is None:
            return self._item.crosspost_parent_list[0]['media']['reddit_video']['fallback_url']
        else:
            return self._item.media['reddit_video']['fallback_url']

    @property
    def _gyfcat_url(self) -> str:
        try:
            return self._item.preview['reddit_video_preview']['fallback_url']
        except BaseException:
            return None

    @property
    def _redgifs_url(self) -> str:
        try:
            return self._item.preview['reddit_video_preview']['fallback_url']
        except BaseException:
            pass

        # need to extract the video link through html requests
        response = requests.get(self._item.url).text
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(response))
        for url in urls:
            if url.endswith('.mp4'):
                return url
        return None

    @property
    def _streamable_url(self) -> str:
        try:
            html = self._item.media['oembed']['html']
            url = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(html))
            return url + '.mp4'
        except BaseException:
            return None

    @property
    def _reddit_gallery_url(self) -> list:
        try:
            metadata = self._item.media_metadata.values()
            return [i['s']['u'] for i in metadata if i['e'] == 'Image']
        except BaseException:
            return None  # deleted post

    @property
    def _imgur_gallery_url(self) -> list:
        try:
            return [self._item.preview['images'][0]['source']['url']]
        except BaseException:
            return None

    @property
    def _mp4_url_from_gif_url(self) -> str:
        ''' Replace .gifv and .gif extensions with .mp4 extension.'''
        return self._item.url.replace('gifv', 'mp4').replace('gif', 'mp4')

    @property
    def _is_comment(self) -> bool:
        if isinstance(self._item, praw.models.reddit.comment.Comment):
            return True
        return False

    @property
    def _is_valid_domain(self) -> bool:
        return True if self._item.domain in self.valid_domains else False

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

    def _is_valid_post(self) -> bool:
        # TODO: think about a more clean way to handle this.
        if self._item is None:
            return False
        if self._item.author is None:
            return False
        if self._item.id is None:
            return False
        if self._is_comment:
            return False
        if not self._is_valid_subreddit:
            return False
        if not self._is_valid_domain:
            return False
        return True

    def get_media_url(self) -> list:
        # TODO: maybe make this into some kind of for loop through
        #       the valid domains?
        if self._item.domain == 'v.redd.it':
            media_url = self._vreddit_url
        elif self._item.domain == 'gfycat.com':
            media_url = self._gyfcat_url
        elif self._item.domain == 'redgifs.com':
            media_url = self._redgifs_url
        elif self._item.domain == 'streamable.com':
            media_url = self._streamable_url
        elif self._item.domain == 'imgur.com' and not self._item.url.endswith(('jpg', 'png')):
            media_url = self._imgur_gallery_url
        elif self._item.url.startswith(utils.REDDIT_GALLERY_URL):
            media_url = self._reddit_gallery_url
        elif self._item.url.endswith('gifv'):
            media_url = self._mp4_url_from_gif_url
        else:
            media_url = self._item.url  # all the png and jpg ready for download
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
                if self.client.args['save_metadata']:
                    self.file_handler.save_metadata(path, str(filename))

                if self.client.args['debug']:
                    utils.print_file_added_debug(filename, path)
                else:
                    utils.print_file_added(filename)
                self.download_counter += 1
        except BaseException:
            if self.client.args['verbose']:
                utils.print_failed(f'While adding file: {filename}')

    def download(self):
        data = self.file_handler.absolute_path
        if isinstance(data, list):
            for d in data:
                filename = self.file_handler.get_filename_from_path(d['path'])
                self.__write__(d['url'], d['path'], filename)
        else:
            filename = self.file_handler.get_filename(self.media_url)
            self.__write__(self.media_url, data, filename)

        if self.client.args['debug']:
            self.file_handler.remove_file
            self.file_handler.delete_database

    def can_download_item(self):
        if self.media_url is None:
            return False

        if self.client.args['only_video'] and not self.file_handler.is_video:
            if self.client.args['verbose']:
                utils.print_skipped_image(
                    self.file_handler.get_filename(self.media_url))
            return False

        if self.client.args['no_video'] and self.file_handler.is_video:
            if self.client.args['verbose']:
                utils.print_skipped_video(
                    self.file_handler.get_filename(self.media_url))
            return False

        if self.file_handler.file_exist:
            if self.client.args['verbose']:
                utils.print_info(
                    f'File exists: {self.file_handler.get_filename(self.media_url)}')
            return False

        # NOTE: DONT DO THIS HERE. REFACTOR ME!
        if not os.path.exists(self.file_handler.get_path()):
            self.file_handler.create_path()
        return True

    def _iterate_items(self, items: 'Upvoted or Saved posts') -> None:
        for item in items:
            self._item = item
            self.items_iterated += 1
            if not self.download_limit_reached() and self._is_valid_post():
                self.media_url = self.get_media_url()
                self.file_handler = FileHandler(self)
                if self.can_download_item():
                    self.download()
        self.__print_counters

    def _check_metadata_request(self):
        options = {
            'get_metadata': None,
            'get_link': 'Link',
            'get_title': 'Title'}
        for opt, val in options.items():
            if self.client.args[opt]:
                handler = FileHandler(self)
                handler.get_metadata(self.client.args[opt], val)
                exit(0)
                return

    def start(self) -> None:
        if self.args['config_prefix']:
            Defaults().set_config_prefix(self.args['config_prefix'])
            exit(0)

        if self.args['config_path']:
            if self.args['config_path'].lower() == 'default':
                Defaults().set_path_to_default()
            else:
                Defaults().set_base_path(str(self.args['config_path']))
            exit(0)

        if self.client.args['nsfw']:
            self.valid_domains = self.sfw_domains.union(self.nsfw_domains)
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
