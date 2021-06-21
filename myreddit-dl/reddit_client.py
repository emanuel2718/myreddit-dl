import configparser
import praw
import utils
import logging
import logging.handlers
from terminal import Terminal
from defaults import Defaults


class RedditClient():

    def __init__(self, arg_dict: dict) -> None:
        self.arg_dict = arg_dict
        self.log = utils.setup_logger(__name__, arg_dict['debug'])
        self.defaults = Defaults()
        self.arg_dict = arg_dict
        self.user_instance = None
        self.__check_config_request()

        self.reddit_instance = self.build_reddit_instance()
        self.__check_instance_validity()

    @property
    def config(self):
        return self.defaults.config

    @property
    def section_name(self):
        return self.defaults.config_section_name

    def build_reddit_instance(self) -> praw.Reddit or None:
        self.log.debug('Building reddit instance')

        if len(self.section_name) == 0:
            Terminal().client_config_setup(self.arg_dict['add_client_hidden'])
            exit(0)


        try:
            instance = praw.Reddit(
                user_agent = 'MyReddit-dl',
                client_id = self.config[self.section_name]['client_id'],
                client_secret = self.config[self.section_name]['client_secret'],
                username = self.config[self.section_name]['username'],
                password = self.config[self.section_name]['password'])

        except BaseException:
            Terminal().client_config_setup(self.arg_dict['add_client_hidden'])
            self.build_reddit_instance()

        try:
            if instance.user.me() is not None:
                self.user_instance = instance.user.me()
                return instance
                # TODO: maybe this is not needed. Make sure the instance is correct elsewhere?
                #if str(instance.user.me()).lower() == self.username:
                    #self.log.info('Reddit Instance build status: OK!')
                    #return instance
                #self.log.info('Error in reddit instance build')
        except BaseException:
            self.log.exception('Reddit instance build status: Failed')
            return None
        return None


    def __check_instance_validity(self) -> None:
        if self.reddit_instance is None:
            Terminal().prompt_client_config_setup(self.arg_dict['add_client_hidden'])
            self.log.info('Client configuration status: Done\n')
            exit(0)
        return

    def __check_config_request(self):
        if self.arg_dict['add_client']:
            Terminal().client_config_setup()
            exit(0)
        if self.arg_dict['change_client']:
            Terminal().change_client()
            #self.set_path_to_default()
            exit(0)
        elif self.arg_dict['config_prefix']:
            self.defaults.set_config_prefix(self.args['config_prefix'])
            exit(0)
        elif self.arg_dict['config_path']:
            if self.args['config_path'].lower() == 'default':
                self.defaults.set_default_config_media_path()
            else:
                self.defaults.set_media_path(str(self.args['config_path']))
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
        return self.user_instance.upvoted(
            limit=self.args['max_depth']) if self.args['upvote'] else None

    @property
    def saves(self) -> 'User saved posts':
        ''' Returns a ListingGenerator of the user saved posts if the
            user asked for the saved files with the (-S --saved) flag.
            Otherwise, return None
        '''
        return self.user_instance.saved(
            limit=self.args['max_depth']) if self.args['saved'] else None


if __name__ == '__main__':
    utils.print_warning(utils.DONT_RUN_THIS_FILE)
