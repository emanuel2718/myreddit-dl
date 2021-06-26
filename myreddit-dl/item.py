from datetime import datetime
import requests


class Item:

    def __init__(self, item):
        self._item = item

    def __len__(self):
        return len(self._item)

    def __getitem__(self):
        return self._item

    def __repr__(self):
        return 'Item(%r, %r, %r, %r %r)' % (self.item_id,
                                            self.title,
                                            self.link,
                                            self.subreddit_prefixed,
                                            self.author)

    def __str__(self):
        fmt = '{:6} = {}\n{:6} = {}\n{:6} = {}\n{:6} = {}\n{:6} = {}'
        return fmt.format('Id', self.item_id,
                          'Title', self.title,
                          'Link', self.link,
                          'Sub', self.subreddit_prefixed,
                          'Author', self.author)

    def get_item(self) -> 'RedditPostItem':
        return self._item

    @property
    def title(self) -> str:
        return str(self._item.title)

    @property
    def item_id(self) -> str:
        return str(self._item.id)

    @property
    def domain(self) -> str:
        return str(self._item.domain)

    @property
    def url(self) -> str:
        return str(self._item.url)

    @property
    def link(self) -> str:
        return 'https://reddit.com' + str(self._item.permalink)

    @property
    def subreddit_name(self) -> str:
        return str(self._item.subreddit)

    @property
    def subreddit_prefixed(self) -> str:
        ''' Returns the item subreddit in the format r/Subreddit'''
        return str(self._item.subreddit_name_prefixed)

    @property
    def upvotes_amount(self) -> str:
        return str(self._item.ups)

    @property
    def author(self) -> str:
        return str(self._item.author)

    def is_nsfw(self) -> bool:
        return self._item.over_18

    def get_creation_date(self) -> str:
        time_utc = self._item.created_utc
        return str(datetime.fromtimestamp(time_utc).strftime('%m/%d/%Y'))

    def get_vreddit_url(self) -> str:
        ''' For the https://v.redd.it posts'''
        if self._item.media is None:
            # if self._item.media is None:
            return self._item.crosspost_parent_list[0]['media']['reddit_video']['fallback_url']
        else:
            return self._item.media['reddit_video']['fallback_url']

    def get_gyfcat_url(self) -> str:
        try:
            return self._item.preview['reddit_video_preview']['fallback_url']
        except BaseException:
            print('gyfact_url exception')
            # self.log.exception('gyfact_url exception raised')
            return None

    def get_redgifs_url(self) -> str:
        try:
            return self._item.preview['reddit_video_preview']['fallback_url']
        except BaseException:
            print('redgifs_url exception raised')
            pass

        # need to extract the video link through html requests
        response = requests.get(self._item.url).text
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(response))
        for url in urls:
            if url.endswith('.mp4'):
                return url
        return None

    def get_streamable_url(self) -> str:
        try:
            html = self._item.media['oembed']['html']
            url = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(html))
            return url + '.mp4'
        except BaseException:
            print('streamable_url exception raised')
            return None

    def get_reddit_gallery_url(self) -> list:
        try:
            metadata = self._item.media_metadata.values()
            return [i['s']['u'] for i in metadata if i['e'] == 'Image']
        except BaseException:
            print('reddit_gallery_url exception raised')
            return None  # deleted post

    def get_imgur_gallery_url(self) -> list:
        try:
            return [self._item.preview['images'][0]['source']['url']]
        except BaseException:
            print('imgur_gallery_url exception raised')
            return None

    def get_mp4_url_from_gif_url(self) -> str:
        ''' Replace .gifv and .gif extensions with .mp4 extension.'''
        return self._item.url.replace('gifv', 'mp4').replace('gif', 'mp4')
