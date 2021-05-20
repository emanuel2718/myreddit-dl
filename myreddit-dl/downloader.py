import cli
import json
import pprint
import praw
import re
import requests
from bs4 import BeautifulSoup
from file_handler import FileHandler


class Downloader:
    def __init__(self, client) -> None:
        self.client = client
        self.args = client.get_args()
        self.username = client.get_user()
        self.upvoted = client.get_user_upvotes()
        self.saved = client.get_user_saves()
        self.subreddit_list = self.args['subreddit']
        self.by_user = self.args['user']
        self.limit = self.args['limit']
        self.valid_domains = self._get_valid_domains()
        self.valid_nsfw_domains = self._get_valid_nsfw_domains()
        self.download_counter = 0
        self.start()

    def _is_gallery_item(self, url):
        if url.startswith('https://www.reddit.com/gallery/'):
            return True
        return False

    def _is_valid_domain(self, domain: str) -> bool:
        return True if domain in self.valid_domains else False

    def _get_valid_domains(self) -> set:
        return {'v.redd.it', 'i.redd.it', 'i.imgur.com', 'gfycat.com', 'streamable.com'}

    def _get_valid_nsfw_domains(self) -> set:
        return {'redgifs.com', 'erome.com'}

    def _get_vreddit_url(self, item):
        ''' For the https://v.redd.it posts'''
        if item.media is None:
            return item.crosspost_parent_list[0]['media']['reddit_video']['fallback_url']
        else:
            return item.media['reddit_video']['fallback_url']

    def _get_gyfcat_url(self, item) -> str or None:
        try:
            return item.preview['reddit_video_preview']['fallback_url']
        except BaseException:
            return None

    def _get_redgifs_url(self, item) -> str or None:
        try:
            return item.preview['reddit_video_preview']['fallback_url']
        except BaseException:
            pass

        # need to extract the video link through html requests
        response = requests.get(item.url).text
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(response))
        for url in urls:
            if url.endswith('.mp4'):
                return url
        return None

    def _get_streamable_url(self, item):
        try:
            html = item.media['oembed']['html']
            url = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(html))
            return url + '.mp4'
        except BaseException:
            return None

    def _iterate_items(self, items):
        for item in items:
            media_url = None
            # Avoid saved comments posts
            if not isinstance(item, praw.models.reddit.comment.Comment):
                if self._is_valid_domain(item.domain):
                    if item.domain == 'v.redd.it':
                        media_url = self._get_vreddit_url(item)
                    if item.domain == 'gfycat.com':
                        media_url = self._get_gyfcat_url(item)
                    if item.domain == 'redgifs.com':
                        media_url = self._get_redgifs_url(item)
                    if item.domain == 'streamable.com':
                        media_url = self._get_streamable_url(item)

    def start(self):
        if self.args['nsfw']:
            self.valid_domains = self.valid_domains.union(self.valid_nsfw_domains)
        if self.args['upvote'] and not self.args['saved']:
            self._iterate_items(self.upvoted)
        elif self.args['saved'] and not self.args['upvote']:
            self._iterate_items(self.saved)
        elif self.args['saved'] and self.args['upvote']:
            print('THREADS: iterating both saved and upvotes')
        else:
            cli.print_error('Specify upvotes (-U, --upvote) or saves (-S, --saved). '
                            'See myreddit-dl --help for more information.')


if __name__ == '__main__':
    cli.print_warning(cli.DONT_RUN_THIS_FILE)
