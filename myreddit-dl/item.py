from datetime import datetime
import requests
import re
import pprint


class Item:

    def __init__(self, item):
        self.__item = item

    def __len__(self):
        return len(self.__item)

    def __getitem__(self):
        return self.__item

    def __repr__(self):
        return 'Item(%r, %r, %r, %r %r)' % (self.get_id(),
                                            self.get_title(),
                                            self.get_reddit_link(),
                                            self.get_subreddit_prefixed(),
                                            self.get_author())

    def __str__(self):
        #pprint.pprint(vars(self.get_item()))
        fmt = '{:6} = {}\n{:6} = {}\n{:6} = {}\n{:6} = {}\n{:6} = {}'
        return fmt.format('Id', self.get_id(),
                          'Title', self.get_title(),
                          'Link', self.get_reddit_link(),
                          'Sub', self.get_subreddit_prefixed(),
                          'Author', self.get_author())

    def get_item(self) -> 'RedditPostItem':
        return self.__item

    def get_title(self) -> str:
        # TODO: hadle unicode here?
        ''' Reddit post title'''
        return str(self.__item.title)

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

    def get_creation_date(self) -> str:
        time_utc = self.__item.created_utc
        return str(datetime.fromtimestamp(time_utc).strftime('%m/%d/%Y'))

    def get_vreddit_url(self) -> str:
        ''' For the https://v.redd.it posts'''
        if self.__item.media is None:
            # if self.__item.media is None:
            return self.__item.crosspost_parent_list[0]['media']['reddit_video']['fallback_url']
        else:
            # TODO: fix this. Some redgifs that don't have preview are causing exceptions
            try:
                return self.__item.media['reddit_video']['fallback_url']
            except:
                return self.__item.media['oembed']['thumbnail_url'].replace('jpg', 'mp4')

    def get_gyfcat_url(self) -> str:
        try:
            return self.__item.preview['reddit_video_preview']['fallback_url']
        except BaseException:
            print('gyfact_url exception')
            # self.log.exception('gyfact_url exception raised')
            return None

    def get_redgifs_url(self) -> str:
        try:
            return self.__item.preview['reddit_video_preview']['fallback_url']
        except BaseException:
            print('redgifs_url exception raised: ')
            pass

        # need to extract the video link through html requests
        response = requests.get(self.__item.url).text
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(response))
        for url in urls:
            if url.endswith('.mp4'):
                return url
        return None

    def get_streamable_url(self) -> str:
        try:
            html = self.__item.media['oembed']['html']
            url = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(html))
            return url + '.mp4'
        except BaseException:
            print('streamable_url exception raised')
            return None

    def get_reddit_gallery_url(self) -> list:
        try:
            metadata = self.__item.media_metadata.values()
            return [i['s']['u'] for i in metadata if i['e'] == 'Image']
        except BaseException:
            print('reddit_gallery_url exception raised')
            return None  # deleted post

    def get_imgur_gallery_url(self) -> list:
        try:
            return [self.__item.preview['images'][0]['source']['url']]
        except BaseException:
            print('imgur_gallery_url exception raised')
            return None

    def get_mp4_url_from_gif_url(self) -> str:
        ''' Replace .gifv and .gif extensions with .mp4 extension.'''
        return self.__item.url.replace('gifv', 'mp4').replace('gif', 'mp4')
