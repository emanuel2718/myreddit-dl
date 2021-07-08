from datetime import datetime
import requests
import re
from pprint import pprint
import praw
import utils


class Item:
    def __init__(self, item):
        self.log = utils.setup_logger(__name__)
        self.__item = item
        self.__media_url = self._fetch_media_url()

    def __len__(self):
        return len(self.__media_url)

    def __getitem__(self):
        return self.__item

    def __repr__(self):
        return 'Item(id=%r, title=%r, link=%r, sub=%r author=%r)' % (self.get_id(),
                                                                     self.get_title(),
                                                                     self.get_reddit_link(),
                                                                     self.get_subreddit_prefixed(),
                                                                     self.get_author())

    def __str__(self):
        return self.fmt.format('-' * 50,
                               'Id', self.get_id(),
                               'Title', self.get_title(),
                               'Link', self.get_reddit_link(),
                               'Domain', self.get_domain(),
                               'Sub', self.get_subreddit_prefixed(),
                               'Author', self.get_author(),
                               'Video', self.is_video(),
                               #'Comment', self.is_comment(),
                               '-' * 50)

    @property
    def __dict__(self):
        # call with vars(item) instead of pprint(vars(item))
        return pprint(vars(self.__item))

    @property
    def fmt(self):
        return ('{}\n'
                '{:6} = {}\n'
                '{:6} = {}\n'
                '{:6} = {}\n'
                '{:6} = {}\n'
                '{:6} = {}\n'
                '{:6} = {}\n'
                '{:6} = {}\n'
                #'{:6} = {}\n'
                '{}\n')

    @property
    def __mapped_domains(self) -> dict:
        return {'v.redd.it': self.get_vreddit_url,
                'gfycat.com': self.get_gfycat_url,
                'redgifs.com': self.get_redgifs_url,
                'streamable.com': self.get_streamable_url,
                'imgur.com': self.get_imgur_url,
                'reddit.com': self.get_reddit_gallery_url

                }

    def get_item(self) -> 'RedditPostItem':
        return self.__item

    def get_title(self) -> str:
        ''' Reddit post title without unicode'''
        return str(self.__item.title).encode('ascii', 'ignore').decode()

    def get_author(self) -> str:
        ''' Reddit post author username'''
        return str(self.__item.author)

    def get_id(self) -> str:
        ''' Reddit post id number'''
        return str(self.__item.id)

    def get_domain(self) -> str:
        ''' Domain in which the media post is hosted'''
        return str(self.__item.domain)

    def get_url(self) -> str:
        ''' Url of the media on the domain is hosted.
            With images it almost always directs to a direct downloable image.
            But with videos, it directs to a non-downloadble source.

        '''
        return str(self.__item.url)

    def get_media_url(self) -> list:
        return self.__media_url

    def get_reddit_link(self) -> str:
        ''' Link of the Reddit post'''
        return 'https://reddit.com' + str(self.__item.permalink)

    def get_subreddit(self) -> str:
        ''' Subreddit name without the r/ prefix'''
        return str(self.__item.subreddit)

    def get_subreddit_prefixed(self) -> str:
        ''' Returns the item subreddit in the format r/Subreddit'''
        return str(self.__item.subreddit_name_prefixed)

    def get_upvotes_amount(self) -> str:
        return str(self.__item.ups)

    def is_nsfw(self) -> bool:
        return self.__item.over_18

    def is_valid_media_post(self) -> bool:
        if self.get_media_url():
            return True
        return False

    def is_video(self) -> bool:
        return self.__item.domain in utils.VIDEO_DOMAINS

    def is_comment(self) -> bool:
        return isinstance(self.__item, praw.models.reddit.comment.Comment)

    def get_creation_date(self) -> str:
        time_utc = self.__item.created_utc
        return str(datetime.fromtimestamp(time_utc).strftime('%m/%d/%Y'))

    def _fetch_media_url(self) -> list:
        ''' Returns a list of media url(s) for the given post item

            @params:
                domain: media domain of current post item (self.item)

                url:    link to the domain where the media is beign stored.
                        This link can't be used for download. Must extract
                        the media url for download.

            @return: list of url(s) containing the downloable media
        '''
        if self.__item.domain in self.__mapped_domains.keys():
            return self.__mapped_domains[self.__item.domain]()
        return [self.__item.url.replace('gifv', 'mp4').replace('gif', 'mp4')]

    def get_vreddit_url(self) -> list:
        ''' Extracts downloadable url for https://v.redd.it domain posts'''
        try:
            return [self.__item.media['reddit_video']['fallback_url']]

        except Exception:
            self.log.debug("vreddit_url: media['reddit_video'] exception")

        try:
            return [self.__item.crosspost_parent_list[0]
                    ['media']['reddit_video']['fallback_url']]

        except Exception:
            self.log.debug("vreddit_url: crosspost_parent_list exception")

        try:
            return [self.__item.media['oembed']
                    ['thumbnail_url'].replace('jpg', 'mp4')]

        except Exception:
            self.log.debug('v.redd.it media url not found. returning []')
            return []

    def get_gfycat_url(self) -> list:
        ''' Extracts downloadable url for https://gfycat.com domain posts'''
        try:
            return [self.__item.preview['reddit_video_preview']['fallback_url']]

        except Exception:
            self.log.debug(
                f'Gfycat_url: item preview exception: {self.__repr__()}')

        try:
            return [self.__item.media['oembed']
                    ['thumbnail_url'].replace('jpg', 'mp4')]

        except Exception:
            self.log.debug('Gfycat_url: media url not found. Returning []')
            return []

    def get_redgifs_url(self) -> list:
        ''' Extracts downloadable url for https://redgifs.com domain posts'''
        try:
            return [self.__item.preview['reddit_video_preview']['fallback_url']]

        except Exception:
            self.log.debug('Redgifs_url: item preview exception')

        try:
            return [self.__item.media['oembed']
                    ['thumbnail_url'].replace('jpg', 'mp4')]

        except Exception:
            self.log.debug(
                'Redgifs_url: item media oembed exception. Requesting data')

        # This is expensive. Only do it if completely neccesary
        # Extract the video link through html requests
        response = requests.get(self.__item.url).text
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(response))
        return [url for url in urls if url.endswith('.mp4')][:1]

    def get_streamable_url(self) -> list:
        # TODO: debug this
        try:
            html = self.__item.media['oembed']['html']
            url = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(html))
            return [url + '.mp4']
        except Exception:
            print('streamable_url exception raised')
            return []

    def get_reddit_gallery_url(self) -> list:
        try:
            metadata = self.__item.media_metadata.values()
            return [i['s']['u'] for i in metadata if i['e'] == 'Image']
        except Exception:
            self.log.debug(
                'reddit_gallery_url: exception raised. post deleted')
            return []

    def get_imgur_url(self) -> list:
        try:
            return [self.__item.preview['images'][0]['source']['url']]
        except Exception:
            self.log.debug('imgur_url: item preview exception.')
        return [self.__item.url.replace('gifv', 'mp4').replace('gif', 'mp4')]
