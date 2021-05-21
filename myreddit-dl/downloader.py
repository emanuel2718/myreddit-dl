import json
import pprint
import praw
import re
import requests
import utils
from file_handler import FileHandler


class Downloader:
    def __init__(self, client) -> None:
        self.client = client
        self.valid_domains = utils.SFW_DOMAINS
        self.download_counter = 0

        self._item = None  # current upvoted or saved post we are looking at.
        self.start()

    @property
    def __print_item(self):
        pprint.pprint(vars(self._item))

    @property
    def sfw_domains(self) -> set:
        return utils.SFW_DOMAINS

    @property
    def nsfw_domains(self) -> set:
        return utils.NSFW_DOMAINS

    def _is_gallery_item(self) -> bool:
        if self._item.url.startswith(utils.REDDIT_GALLERY_DOMAIN):
            return True
        return False

    def _is_valid_domain(self) -> bool:
        return True if self._item.domain in self.valid_domains else False

    @property
    def _vreddit_url(self) -> list[str]:
        ''' For the https://v.redd.it posts'''
        if self._item.media is None:
            return [self._item.crosspost_parent_list[0]
                    ['media']['reddit_video']['fallback_url']]
        else:
            return [self._item.media['reddit_video']['fallback_url']]

    @property
    def _gyfcat_url(self) -> list[str]:
        try:
            return [self._item.preview['reddit_video_preview']['fallback_url']]
        except BaseException:
            return []

    @property
    def _redgifs_url(self) -> list[str]:
        try:
            return [item.preview['reddit_video_preview']['fallback_url']]
        except BaseException:
            pass

        # need to extract the video link through html requests
        response = requests.get(self._item.url).text
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(response))
        for url in urls:
            if url.endswith('.mp4'):
                return [url]
        return []

    @property
    def _streamable_url(self) -> list[str]:
        try:
            html = self._item.media['oembed']['html']
            url = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(html))
            return [url + '.mp4']
        except BaseException:
            return []

    @property
    def _reddit_gallery_url(self) -> list[(str, str), ...]:
        ''' Returns a list of dual strings tuples. The tuples contains the url and the
            extension of the image as image/jpg or image/png.
        '''
        try:
            metadata = self._item.media_metadata.values()
            return [(i['s']['u'], i['m']) for i in metadata if i['e'] == 'Image']
        except BaseException:
            return []  # deleted post

    @property
    def _imgur_gallery_url(self) -> list[str, ...]:
        try:
            return self._item.preview['images'][0]['source']['url']
        except BaseException:
            return []

    @property
    def _mp4_url_from_gif_url(self) -> list[str]:
        ''' Replace .gifv and .gif extensions with .mp4 extension.'''
        return [self._item.url.replace('gifv', 'mp4').replace('gif', 'mp4')]

    def get_media_url(self) -> list[str, ...]:
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
            media_url = [self._item.url]  # all the png and jpg ready for download
        print(media_url)
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
            media_url = []
            # Avoid saved comments posts
            if not isinstance(item, praw.models.reddit.comment.Comment):
                self._item = item
                if self._is_valid_domain():
                    media_url = self.get_media_url()
                else:
                    pass
                    #print(f'Domain: {self._item.domain} || Url: {self._item.url}')
                    # print(self._item.url)

    def start(self):
        if self.client.args['nsfw']:
            self.valid_domains = self.sfw_domains.union(self.nsfw_domains)
        if self.client.args['upvote'] and not self.client.args['saved']:
            self._iterate_items(self.client.upvotes)
        elif self.client.args['saved'] and not self.client.args['upvote']:
            self._iterate_items(self.client.saves)
        elif self.client.args['saved'] and self.client.args['upvote']:
            print('THREADS: iterating both saved and upvotes')
        else:
            utils.print_error('Specify upvotes (-U, --upvote) or saves (-S, --saved). '
                            'See myreddit-dl --help for more information.')


if __name__ == '__main__':
    utils.print_warning(cli.DONT_RUN_THIS_FILE)
