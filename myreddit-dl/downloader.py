import cli
import json
import pprint
import praw
import re
import requests
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
        self.valid_domains = self._get_valid_sfw_domains()
        self.valid_nsfw_domains = self._get_valid_nsfw_domains()
        self.download_counter = 0
        self._item = None
        self.start()

    def _is_gallery_item(self) -> bool:
        if self._item.url.startswith('https://www.reddit.com/gallery/'):
            return True
        return False

    def _is_valid_domain(self) -> bool:
        return True if self._item.domain in self.valid_domains else False

    def _get_valid_sfw_domains(self) -> set:
        return {'v.redd.it', 'i.redd.it', 'i.imgur.com', 'gfycat.com', 'streamable.com'}

    def _get_valid_nsfw_domains(self) -> set:
        return {'redgifs.com', 'erome.com'}

    def _get_vreddit_url(self):
        ''' For the https://v.redd.it posts'''
        if self._item.media is None:
            return self._item.crosspost_parent_list[0]['media']['reddit_video']['fallback_url']
        else:
            return self._item.media['reddit_video']['fallback_url']

    def _get_gyfcat_url(self) -> str or None:
        try:
            return self._item.preview['reddit_video_preview']['fallback_url']
        except BaseException:
            return None

    def _get_redgifs_url(self) -> str or None:
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

    def _get_streamable_url(self) -> str or None:
        try:
            html = self._item.media['oembed']['html']
            url = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(html))
            return url + '.mp4'
        except BaseException:
            return None

    def _get_mp4_from_gifs(self) -> str:
        ''' Replace .gifv and .gif extensions with .mp4 extension.'''
        return self._item.url.replace('gifv', 'mp4').replace('gif', 'mp4')

    def get_media_url_from_domain(self) -> str:
        if self._item.domain == 'v.redd.it':
            media_url = self._get_vreddit_url()
        elif self._item.domain == 'gfycat.com':
            media_url = self._get_gyfcat_url()
        elif self._item.domain == 'redgifs.com':
            media_url = self._get_redgifs_url()
        elif self._item.domain == 'streamable.com':
            media_url = self._get_streamable_url()
        elif self._item.url.endswith(('gif', 'gifv')):
            media_url = self._get_mp4_from_gifs()
        else:
            media_url = self._item.url
        # TODO: Handle Gallery case: https://www.reddit.com/gallery/ltvpmj
        #       Some galleries contain more than 10 photos or videos. What to do?
        #       Ignore the reddit.com/r/Subreddit/comments posts.

        # TODO: Handle Imgur gallery case: https://imgur.com/a/oOnxxk3/
        #       There are cases where the imgur.com/ ends with .gifv and or png
        #       those cases should be easy to handle. The problem lies in the galleries.
        #       Maybe requests to the rescue?
        #
        # TODO: Handle: https://www.twitch.tv/mande/clip/ImpossibleHilariousOrcaCurseLit-QsfyEix6y5zaCMMN?filter=clips&range=7d&sort=time
        #       Adding .mp4 to the end might solve it. Havent' tried with GET

        # TODO: Handle: https://clips.twitch.tv/SeductiveMagnificentNikudonRaccAttack-dvnHYTkEyOvqaExq
        #       Adding .mp4 makes the clip go missing

    def _iterate_items(self, items):
        for item in items:
            media_url = None
            # Avoid saved comments posts
            if not isinstance(item, praw.models.reddit.comment.Comment):
                self._item = item
                if self._is_valid_domain():
                    media_url = self.get_media_url_from_domain()
                else:
                    print(self._item.url)

                

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
