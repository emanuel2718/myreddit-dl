from pprint import pprint
import utils
import console_args
from reddit_client import RedditClient
from item import Item
from defaults import Defaults

class Downloader(RedditClient):
    def __init__(self):
        super().__init__()
        self.log = utils.setup_logger(__name__)
        self.item = None
        self.defaults = Defaults()

    @property
    def args(self):
        return console_args.get_args()

    def __iterate_items(self, client_items: 'Upvoted and/or Saved posts') -> None:
        for post in client_items:
            self.item = Item(post)
            print(self.item)



    def start(self) -> None:
        if self.args['upvote']:
            self.__iterate_items(self.client_upvotes)
        elif self.args['saved']:
            self.__iterate_items(self.client_saves)
        else:
            utils.print_error(utils.MISSING_DOWNLOAD_SOURCE)



if __name__ == '__main__':
    utils.print_warning(cli.DONT_RUN_THIS_FILE)
