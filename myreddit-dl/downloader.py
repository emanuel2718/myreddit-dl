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
        self.log.debug("Client: %s seconds" % (time.time() - self.client_time))
        self.log = utils.setup_logger(__name__)
        self.args = console_args.get_console_args()
        self.item = None
        self.valid_domains = None
        self.items_iterated = 0
        self.defaults = Defaults()

    @property
    def get_args(self):
        ''' Command-line arguments'''
        return self.args

    @property
    def __mapped_domains(self) -> dict:
        return {'v.redd.it': self.item.get_vreddit_url,
                'gfycat.com': self.item.get_gyfcat_url,
                'redgifs.com': self.item.get_redgifs_url,
                'streamable.com': self.item.get_streamable_url,
                'imgur.com': self.item.get_imgur_gallery_url
                }

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

    def get_media_url(self) -> list:
        ''' Returns a list of media url(s) for the given post item

            @params:
                domain: media domain of current post item (self.item)

                url:    link to the domain where the media is beign stored.
                        This link can't be used for download. Must extract
                        the media url for download.

            @return: list of url(s) containing the downloable media
        '''
        domain, url = self.item.get_domain(), self.item.get_url()
        if domain in self.__mapped_domains.keys():
            return self.__mapped_domains[domain]()
        elif url.startswith(utils.REDDIT_GALLERY_URL):
            return self.item.get_reddit_gallery_url()
        elif url.endswith('gifv'):
            return self.item.get_mp4_url_from_gif_url()
        return [url]

    def __iterate_items(self, client_items: 'Upvoted and/or Saved posts') -> None:
        for post in client_items:
            self.item = Item(post)
            self.items_iterated += 1

        self.log.debug(f'Items iterated: {self.items_iterated}')
        # TODO: Finish me!

    def start(self) -> None:
        self.valid_domains = self.get_valid_domains()

        if self.args['upvote']:
            self.__iterate_items(self.client_upvotes)
        elif self.args['saved']:
            self.__iterate_items(self.client_saves)
        else:
            utils.print_error(utils.MISSING_DOWNLOAD_SOURCE)

        self.log.debug("Total time: %s seconds" % (time.time() - self.client_time))


if __name__ == '__main__':
    utils.print_warning(cli.DONT_RUN_THIS_FILE)
