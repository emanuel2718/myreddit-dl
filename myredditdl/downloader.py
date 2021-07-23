import time
import requests

import myredditdl.console_args as console_args
import myredditdl.utils as utils
from myredditdl.defaults import Defaults
from myredditdl.file_handler import FileHandler
from myredditdl.item import Item
from myredditdl.reddit_client import RedditClient
from myredditdl.metadata_handler import Metadata


class Downloader(RedditClient):
    def __init__(self):
        super().__init__()
        self.args = console_args.get_console_args()
        self.log = utils.setup_logger(__name__, self.args['debug'])
        self.item = None
        self.valid_domains = None
        self.items_downloaded = 0
        self.items_iterated = 0
        self.items_skipped = 0
        self.defaults = Defaults(self.args['debug'])
        self.file_handler = FileHandler()
        self.metadata_handler = Metadata()

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
        ''' Returns a set of SFW domains'''
        return {'v.redd.it',
                'i.redd.it',
                'i.imgur.com',
                'gfycat.com',
                'streamable.com',
                'reddit.com',
                'imgur.com'}

    def __nsfw_domains(self) -> set:
        ''' Returns a set of NSFW domains'''
        return {'redgifs.com', 'erome.com'}

    def download_limit_reached(self) -> bool:
        ''' Checks if the download limit has been reached.
            Download limit it's dictated by the --limit [int] flag.
            If the number of items downloaded reaches the limit set by the user,
            then return True.
            If no --limit flag was given this function always returns False
        '''
        if self.args['limit'] and self.items_downloaded >= self.args['limit']:
            return True
        return False  # Download limit hasn't been reached or no limit was given

    def is_valid_domain(self) -> bool:
        ''' Returns True if the domain of the current item is valid. False otherwise'''
        return self.item.get_domain() in self.valid_domains

    def is_valid_subreddit(self) -> bool:
        ''' Checks whether the current item subreddit is valid or not.
            If the user gave the --sub flag then only the items that belongs
            to the given subreddit(s) will be valid. If no --sub flag
            was given then all the items will have valid subreddits
        '''
        if self.args['sub'] is None:
            return True
        return self.item.get_subreddit().lower() in self.args['sub']

    def can_download(self) -> bool:
        ''' Checks if the item can be downloaded or not
            Invalid Items that can't be downloaded:
                - Empty items
                - Gallery item and --no-gallery flag given
                - Video item and --no-video flag given
                - Image item and --only-video flag given
                - File has already been downloaded before

        @return: True if can download; False otherwise
        '''
        if len(self.item) == 0: # empty item
            return False
        if len(self.item) > 1 and self.args['no_gallery']:
            return False
        if self.args['only_video'] and not self.item.is_video():
            return False
        if self.args['no_video'] and self.item.is_video():
            return False
        if self.file_handler.file_exists():
            self.log.info('Item exists')
            return False
        return True

    def download_item(self) -> None:
        ''' Downloads the item from using the downloable url of the item'''
        data = self.get_data()
        for i in range(len(self.item)):
            r = requests.get(data[i].get('url'))
            with open(data[i].get('path'), 'wb') as f:
                f.write(r.content)
                self.log.info(
                    f'Item added: {self.file_handler.get_filename(i)}')

    def __check_if_metadata_save(self) -> bool:
        ''' Checks if the user gave the --no-metadata flag and if the
            flag wasn't given then add the item data to the metadata_handler
            data structure.
        '''
        if not self.args['no_metadata']:
            filename = self.file_handler.get_filename(0)
            self.metadata_handler.add_to_map(filename,
                                             self.item.get_metadata())
            return True
        return False

    def get_data(self) -> list:
        ''' Returns a list that contains a dictionary of url and filepath pairs.
            The reason for it being a list is that some reddit post are gallery media
            items (i.e more than one media file per item), hence in the case of a gallery
            item we need to iterate through all the gallery media url/paths.

        @return: List of dictionary pairs of url:filepath
                (can be more than one pair per list)
        '''
        return [{'url': self.item.get_media_url()[i],
                 'path': self.file_handler.absolute_path[i]}
                for i in range(len(self.item))]

    def __iterate_items(self, items: 'Upvoted and/or Saved posts') -> None:
        ''' Iterate through the user reddit upvoted and/or saved @items
            and call for download the @items that meet the criteria for download.

        @param:
            - items: User Reddit Upvoted and/or Saved media posts

        '''
        for post_item in items:
            if self.download_limit_reached():
                break
            self.item = Item(post_item)
            self.items_iterated += 1
            if self.is_valid_domain() and self.is_valid_subreddit():
                self.file_handler.set_current_item(self.item)
                if self.can_download():
                    self.download_item()
                    self.__check_if_metadata_save()
                    self.items_downloaded += 1
            else:
                self.items_skipped += 1

    def start(self) -> None:
        ''' Main downloader driver'''
        if not self.build_reddit_instance():
            return

        self.valid_domains = self.get_valid_domains()

        if self.args['upvote']:
            self.__iterate_items(self.client_upvotes)
        elif self.args['saved']:
            self.__iterate_items(self.client_saves)
        else:
            self.log.error(utils.MISSING_DOWNLOAD_SOURCE)

        if self.args['debug']:
            self.file_handler.debug_clean()

        if not self.args['no_metadata']:
            self.file_handler.write_metadata(self.metadata_handler.get_map())

        self.log.info(self)


if __name__ == '__main__':
    print(utils.DONT_RUN_THIS_FILE)
