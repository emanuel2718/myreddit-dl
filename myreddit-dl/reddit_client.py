import configparser
import praw

class RedditClient:

    def __init__(self, args: dict) -> None:
        self.args = args
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # NOTE: self.user is None if config file is empty
        self.reddit_instance = self.build_reddit_instance()
        self.user = self.reddit_instance.user.me()
        self.check_if_valid_user()


    def build_reddit_instance(self) -> praw.Reddit:
        return praw.Reddit(
            user_agent='MyReddit-dl',
            client_id=self.config['REDDIT']['client_id'],
            client_secret=self.config['REDDIT']['client_secret'],
            username=self.config['REDDIT']['username'],
            password=self.config['REDDIT']['password'])

    def get_user(self) -> str:
        return str(self.user)

    def get_args(self) -> dict:
        return self.args

    def check_if_valid_user(self) -> None:
        if self.user:
            return
        util.print_error(util.USER_NOT_FOUND)
        exit(1)

    def get_user_upvotes(self) -> praw.models.listing.generator.ListingGenerator:
        ''' Returns a ListingGenerator of the user upvoted posts if the
            user asked for the saved files with the (-U --upvote) flag.
            Otherwise, return None
        '''
        return self.user.upvoted(limit=None) if self.args['upvote'] else None

    def get_user_saves(self) -> praw.models.listing.generator.ListingGenerator:
        ''' Returns a ListingGenerator of the user saved posts if the
            user asked for the saved files with the (-S --saved) flag.
            Otherwise, return None
        '''
        return self.user.saved(limit=None) if self.args['saved'] else None

if __name__ == '__main__':
    cli.print_warning(cli.DONT_RUN_THIS_FILE)
