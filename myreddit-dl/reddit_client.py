import time
import configparser
import console_args
import praw
import utils
import logging
import logging.handlers
#from terminal import Terminal
from config_handler import ConfigHandler
from defaults import Defaults


class RedditClient:
    def __init__(self) -> None:
        self.client_time = time.time()
        self.logger = utils.setup_logger(__name__)
        self.conf = ConfigHandler()
        self.arg_dict = console_args.get_console_args()
        self.user_instance = None


    @property
    def section_name(self):
        return self.conf.get_client_username()

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
        return self.user_instance.upvoted(
            limit=self.arg_dict['max_depth']) if self.arg_dict['upvote'] else None

    @property
    def client_saves(self) -> 'User saved posts':
        ''' Yields a ListingGenerator of the user saved posts if the
            user asked for the saved files with the (-S --saved) flag.
            Otherwise, return None
        '''
        return self.user_instance.saved(
            limit=self.arg_dict['max_depth']) if self.arg_dict['saved'] else None


    def build_reddit_instance(self) -> bool:
        self.logger.info('Building reddit instance...')

        if len(self.section_name) == 0:
            self.logger.warning('No valid clients were found.'
                             'Add new reddit clients with the --add-client flag')
            return False

        try:
            self.user_instance = praw.Reddit(
                user_agent='myreddit-dl',
                client_id=self.config[self.section_name]['client_id'],
                client_secret=self.config[self.section_name]['client_secret'],
                username=self.config[self.section_name]['username'],
                password=self.config[self.section_name]['password']).user.me()

        except Exception:
            self.logger.error('Reddit instance build: Failed!')
            return False

        self.logger.debug("Client: %s seconds" % (time.time() - self.client_time))
        return True



    @classmethod
    def validate_instance(cls, instance: dict) -> bool:
        try:
            instance = praw.Reddit(
                user_agent='myreddit-dl',
                client_id=instance.get('client_id'),
                client_secret=instance.get('client_secret'),
                username=instance.get('username'),
                password=instance.get('password')).user.me()
            return True

        except Exception:
            print('INFO: instance validator: Failed!')

        return False


    #def build_reddit_instance(self) -> praw.Reddit or None:
    #    self.log.debug('Building reddit instance')

    #    #if len(self.section_name) == 0:
    #    #    Terminal().client_config_setup(self.arg_dict['add_client_hidden'])
    #    #    exit(0)

    #    try:
    #        instance = praw.Reddit(
    #            user_agent='MyReddit-dl',
    #            client_id=self.config[self.section_name]['client_id'],
    #            client_secret=self.config[self.section_name]['client_secret'],
    #            username=self.config[self.section_name]['username'],
    #            password=self.config[self.section_name]['password'])

    #    except Exception:
    #        print('error building')
    #        #Terminal().client_config_setup(self.arg_dict['add_client_hidden'])
    #        #self.build_reddit_instance()

    #    try:
    #        if instance.user.me() is not None:
    #            self.user_instance = instance.user.me()
    #            self.log.debug("Client: %s seconds" % (time.time() - self.client_time))
    #            return instance
    #            # TODO: maybe this is not needed. Make sure the instance is correct elsewhere?
    #            # if str(instance.user.me()).lower() == self.username:
    #            #self.log.info('Reddit Instance build status: OK!')
    #            # return instance
    #            #self.log.info('Error in reddit instance build')
    #    except BaseException:
    #        self.log.exception('Reddit instance build status: Failed')
    #        return None
    #    return None

    #def __check_instance_validity(self) -> None:
    #    if self.reddit_instance is None:
    #        Terminal().prompt_client_config_setup(
    #            self.arg_dict['add_client_hidden'])
    #        self.log.info('Client configuration status: Done\n')
    #        exit(0)
    #    return

    #def __check_config_request(self):
    #    # TODO: Terminal was change to cli
    #    if self.arg_dict['add_client']:
    #        Terminal().client_config_setup()
    #        exit(0)
    #    if self.arg_dict['change_client']:
    #        Terminal().change_client()
    #        # self.set_path_to_default()
    #        exit(0)
    #    elif self.arg_dict['config_prefix']:
    #        self.defaults.set_config_prefix(self.arg_dict['config_prefix'])
    #        exit(0)
    #    elif self.arg_dict['config_path']:
    #        if self.arg_dict['config_path'].lower() == 'default':
    #            self.defaults.set_default_config_media_path()
    #        else:
    #            self.defaults.set_media_path(str(self.arg_dict['config_path']))
    #        exit(0)
    #    elif self.arg_dict['get_config']:
    #        Terminal().print_config_data()
    #        exit(0)
    #    elif self.arg_dict['get_config_show']:
    #        Terminal().print_config_data(True)
    #        exit(0)
    #    return


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
