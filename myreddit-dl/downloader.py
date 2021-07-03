from pprint import pprint
import console_args
import utils
import time
import praw
from reddit_client import RedditClient
from item import Item
from defaults import Defaults


class Downloader(RedditClient):
    def __init__(self):
        super().__init__()
        self.log = utils.setup_logger(__name__)
        self.args = console_args.get_console_args()
        self.item = None
        self.items_iterated = 0
        self.items_downloaded = 0
        self.items_skipped = 0
        self.valid_domains = None
        self.defaults = Defaults()

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
        return self.args['sub'] is None or self.item.get_subreddit().lower() in self.args['sub']


    def __iterate_items(
            self,
            client_items: 'Upvoted and/or Saved posts') -> None:
        for post in client_items:
            if self.download_limit_reached():
                break
            self.item = Item(post)
            self.items_iterated += 1
            if self.is_valid_domain() and self.is_valid_subreddit():
                print(self.item.get_media_url())
                # TODO: Finish me!

    def start(self) -> None:
        self.valid_domains = self.get_valid_domains()

        if self.args['upvote']:
            self.__iterate_items(self.client_upvotes)
        elif self.args['saved']:
            self.__iterate_items(self.client_saves)
        else:
            utils.print_error(utils.MISSING_DOWNLOAD_SOURCE)

        self.log.debug(self)


if __name__ == '__main__':
    print(utils.DONT_RUN_THIS_FILE)
