import json
import os
import pprint
import praw
import re
import requests
import utils
from file_handler import FileHandler


class Downloader:
    def __init__(self, client: 'RedditClient') -> None:
        self.client = client
        self.valid_domains = utils.SFW_DOMAINS
        self.download_counter = 0

        self._item = None  # current upvoted or saved post we are looking at.
        self.media_url = None
        self.start()

    @property
    def __print_item(self) -> None:
        pprint.pprint(vars(self._item))

    @property
    def item(self) -> 'RedditPostItem':
        return self._item

    @property
    def user(self) -> str:
        return str(self.client.user)

    @property
    def args(self) -> dict:
        return self.client.args

    @property
    def subreddit(self) -> str:
        return self._item.subreddit

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
            return item.preview['reddit_video_preview']['fallback_url']
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
        if self.client.args['subreddit'] is None:
            return True
        return self.subreddit in self.client.args['subreddit']

    def _is_valid_post(self) -> bool:
        # TODO: think about a more clean way to handle this.
        if self._item is None:
            return False
        if self._item.author is None:
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
        elif self._item.url.endswith(('gif', 'gifv')):
            media_url = self._mp4_url_from_gif_url
        else:
            media_url = self._item.url  # all the png and jpg ready for download
        return media_url

    def download_limit_reached(self) -> bool:
        if self.args['limit'] and self.download_counter >= self.args['limit']:
            exit(1)
            return True
        return False

    def __write__(self, path) -> None:
        if self.media_url is None:
            return

        # This are gallery posts (multiple media per post)
        if isinstance(path, list):
            for p in path:
                r = requests.get(p[0])
                try:
                    with open(p[1], 'wb') as f:
                        f.write(r.content)
                        utils.print_file_added(p[1])
                except BaseException:
                    if self.client.args['verbose']:
                        utils.print_failed(f'Adding file: {p[1]}')
        else:
            r = requests.get(self.media_url)
            try:
                with open(path, 'wb') as f:
                    f.write(r.content)
                    utils.print_file_added(path)
            except BaseException:
                if self.client.args['verbose']:
                    utils.print_failed(f'Adding file : {path}')

    def download(self, base_path: str, abs_path: str) -> None:
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        self.__write__(abs_path)
        self.download_counter += 1

    def _iterate_items(self, items: 'Upvoted or Saved posts') -> None:
        for item in items:
            self._item = item
            if not self.download_limit_reached() and self._is_valid_post():
                self.media_url = self.get_media_url()
                handler = FileHandler(self)
                base_path = handler.base_path
                absolute_path = handler.absolute_path
                filename = handler.get_filename(self.media_url)
                if handler.file_exist(absolute_path):
                    if self.client.args['verbose']:
                        utils.print_info(f'File exist: {filename}')
                    continue
                self.download(base_path, absolute_path)

        if self.client.args['debug']:
            utils.print_info(f'{self.download_counter} items downloaded.')

    def start(self) -> None:
        if self.client.args['nsfw']:
            self.valid_domains = self.sfw_domains.union(self.nsfw_domains)
        if self.client.args['upvote'] and not self.client.args['saved']:
            self._iterate_items(self.client.upvotes)
        elif self.client.args['saved'] and not self.client.args['upvote']:
            self._iterate_items(self.client.saves)
        elif self.client.args['saved'] and self.client.args['upvote']:
            print('THREADS: iterating both saved and upvotes')
        else:
            utils.print_error('Specify upvoted (-U, --upvote) or saved (-S, --saved) posts. '
                              'See myreddit-dl --help for more information.')


if __name__ == '__main__':
    utils.print_warning(cli.DONT_RUN_THIS_FILE)
