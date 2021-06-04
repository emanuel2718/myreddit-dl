import configparser
import praw
import utils


class RedditClient:

    def __init__(self, arg_dict: dict) -> None:
        self.arg_dict = arg_dict
        self.config = configparser.ConfigParser()
        self.config.read(utils.CFG_FILENAME)

        self.username = None
        self.reddit_instance = self.build_reddit_instance()

    def build_reddit_instance(self) -> praw.Reddit:
        instance = praw.Reddit(
            user_agent='MyReddit-dl',
            client_id=self.config['REDDIT']['client_id'],
            client_secret=self.config['REDDIT']['client_secret'],
            username=self.config['REDDIT']['username'],
            password=self.config['REDDIT']['password'])
        try:
            self.username = instance.user.me()
            utils.print_info('Reddit Instance build status: OK!\n')
            return instance

        except BaseException:
            utils.print_info('Reddit Instance build status: Failed.')
            utils.print_error(utils.USER_NOT_FOUND)
            exit(1)

    @property
    def max_depth(self):
        return self.arg_dict['max_depth']

    @property
    def user(self) -> str:
        return str(self.username)

    @property
    def args(self) -> dict:
        return self.arg_dict

    @property
    def upvotes(self) -> 'User upvoted posts':
        ''' Returns a ListingGenerator of the user upvoted posts if the
            user asked for the saved files with the (-U --upvote) flag.
            Otherwise, return None
        '''
        return self.username.upvoted(
            limit=self.args['max_depth']) if self.args['upvote'] else None

    @property
    def saves(self) -> 'User saved posts':
        ''' Returns a ListingGenerator of the user saved posts if the
            user asked for the saved files with the (-S --saved) flag.
            Otherwise, return None
        '''
        return self.username.saved(
            limit=self.args['max_depth']) if self.args['saved'] else None


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
