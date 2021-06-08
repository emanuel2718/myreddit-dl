import configparser
import praw
import utils
import logging
import logging.handlers
from terminal import Terminal


class RedditClient:

    def __init__(self, arg_dict: dict) -> None:
        self.log = utils.setup_logger(__name__, arg_dict['debug'])
        self.arg_dict = arg_dict
        self.config = configparser.ConfigParser()
        self.config.read(utils.CFG_FILENAME)
        self.__check_config_request()

        self.username = None
        self.reddit_instance = self.build_reddit_instance()
        self.__check_instance_validity()

    def build_reddit_instance(self) -> praw.Reddit or None:
        self.log.debug('Building reddit instance')
        instance = praw.Reddit(
            user_agent='MyReddit-dl',
            client_id=self.config['REDDIT']['client_id'],
            client_secret=self.config['REDDIT']['client_secret'],
            username=self.config['REDDIT']['username'],
            password=self.config['REDDIT']['password'])

        try:
            if instance.user.me() is not None:
                self.username = instance.user.me()
                self.log.info('Reddit Instance build status: OK!')
                return instance
        except BaseException:
            self.log.exception('Reddit instance build status: Failed')
            return None
        return None

    def __check_instance_validity(self) -> None:
        if self.reddit_instance is None:
            Terminal().prompt_client_config_setup()
            self.log.info('Client configuration status: Done\n\n')
            self.__init__(self.arg_dict)
        return

    def __check_config_request(self):
        if self.arg_dict['config_client']:
            Terminal().client_config_setup()
            exit(0)
        elif self.arg_dict['config_prefix']:
            from defaults import Defaults
            Defaults().set_config_prefix(self.args['config_prefix'])
            exit(0)
        elif self.arg_dict['config_path']:
            from defaults import Defaults
            if self.args['config_path'].lower() == 'default':
                Defaults().set_path_to_default()
            else:
                Defaults().set_base_path(str(self.args['config_path']))
            exit(0)
        elif self.arg_dict['get_config']:
            Terminal().print_config_data()
            exit(0)
        elif self.arg_dict['get_config_show']:
            Terminal().print_config_data(True)
            exit(0)
        return

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
