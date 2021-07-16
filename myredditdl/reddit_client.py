import time
import praw
import myredditdl.console_args as console_args
import myredditdl.utils as utils
from myredditdl.config_handler import ConfigHandler


class RedditClient:
    def __init__(self) -> None:
        self.client_time = time.time()
        self.arg_dict = console_args.get_console_args()
        self.logger = utils.setup_logger(__name__, self.arg_dict['debug'])
        self.conf = ConfigHandler()
        self.user_instance = None

    @property
    def section_name(self):
        return self.conf.get_client_active_section()

    @property
    def config(self):
        return self.conf.get_config()

    @property
    def max_depth(self):
        return self.arg_dict['max_depth']

    @property
    def client_upvotes(self) -> 'User upvoted posts':
        ''' Yields a ListingGenerator of the user upvoted posts if the
            user asked for the saved files with the (-U --upvote) flag.
            Otherwise, return None
        '''
        if self.user_instance is None:
            self.logger.warning('User instance is None. Fix me!')
            return ()
        return self.user_instance.upvoted(
            limit=self.arg_dict['max_depth']) if self.arg_dict['upvote'] else None

    @property
    def client_saves(self) -> 'User saved posts':
        ''' Yields a ListingGenerator of the user saved posts if the
            user asked for the saved files with the (-S --saved) flag.
            Otherwise, return None
        '''
        if self.user_instance is None:
            self.logger.warning('User instance is None. Fix me!')
            return ()
        return self.user_instance.saved(
            limit=self.arg_dict['max_depth']) if self.arg_dict['saved'] else None

    def build_reddit_instance(self) -> bool:
        self.logger.info('Building reddit instance...')

        if len(self.section_name) == 0:
            self.logger.warning(
                'No valid clients were found.'
                'Add new reddit clients with the --add-client flag')
            return False

        try:
            self.user_instance = praw.Reddit(
                user_agent='myredditdl',
                client_id=self.config[self.section_name]['client_id'],
                client_secret=self.config[self.section_name]['client_secret'],
                username=self.config[self.section_name]['username'],
                password=self.config[self.section_name]['password']).user.me()

        except Exception:
            self.logger.error('Reddit instance build: Failed!')
            return False

        self.logger.debug(
            "Client: %s seconds" %
            (time.time() - self.client_time))
        return True

    @classmethod
    def validate_instance(cls, instance: dict) -> bool:
        try:
            instance = praw.Reddit(
                user_agent='myredditdl',
                client_id=instance.get('client_id'),
                client_secret=instance.get('client_secret'),
                username=instance.get('username'),
                password=instance.get('password')).user.me()
            return True

        except Exception:
            print('INFO: instance validator: Failed!')

        return False


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
