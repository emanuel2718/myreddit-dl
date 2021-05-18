import util
import configparser
import praw


class RedditClient:

    def __init__(self, args):
        self.args = args
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # NOTE: self.reddit_instance.user.me() is None if config file is empty
        self.reddit_instance = self.build_reddit_instance()
        self.user = self.reddit_instance.user.me()

        self.check_if_valid_user()

        self.upvoted = self.get_user_upvotes()
        self.saved = self.get_user_saves()
        print(self.upvoted)
        print(self.saved)

    def build_reddit_instance(self):
        return praw.Reddit(
            user_agent='MyReddit-dl',
            client_id=self.config['REDDIT']['client_id'],
            client_secret=self.config['REDDIT']['client_secret'],
            username=self.config['REDDIT']['username'],
            password=self.config['REDDIT']['password'])

    def check_if_valid_user(self):
        if self.user:
            return
        util.print_error(util.USER_NOT_FOUND)
        exit(1)

    def get_user_upvotes(self):
        ''' Returns a ListingGenerator of the user upvoted posts if the
            user asked for the saved files with the (-U --upvote) flag.
            Otherwise, return None
        '''
        return self.user.upvoted(limit=None) if self.args['upvote'] else None

    def get_user_saves(self):
        ''' Returns a ListingGenerator of the user saved posts if the
            user asked for the saved files with the (-S --saved) flag.
            Otherwise, return None
        '''
        return self.user.saved(limit=None) if self.args['saved'] else None


def run_cli(args):
    cli_client = RedditClient(args)
    print('Running from CLI from myreddit-dl.py')


if __name__ == '__main__':
    util.print_warning(util.DONT_RUN_THIS_FILE)
