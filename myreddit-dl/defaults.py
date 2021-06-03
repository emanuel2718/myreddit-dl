import utils
import configparser
import os


class Defaults:
    def __init__(self, debug=False) -> None:
        self.debug = debug
        self.config = configparser.ConfigParser()
        #self.HOME_DIR = os.path.expanduser('~')
        #self.DEFAULT_DIR = self.HOME_DIR + os.sep + 'Pictures'
        #self.BASE_PATH = self._parse_path()

    def set_config_save(self, save_as: str) -> None:
        if save_as.lower() != utils.CFG_SAVE_DEFAULT and save_as.lower() != 'username':
            utils.print_error(utils.INVALID_CFG_OPTION)
            return

        self.config.read(utils.CFG_FILE)
        if save_as.lower() == self.config['SAVE']['filename_save']:
            utils.print_info('This is already the current set saving option.')
            return

        # Different valid option given (username or subreddit)
        try:
            self.config.set('SAVE', 'filename_save', save_as)
            with open(utils.CFG_FILE, 'w') as config_file:
                self.config.write(config_file)
            utils.print_info('Save format changed succesfully.')

        except BaseException:
            utils.print_error(
                'Something went wrong changing the saving format.')
            exit(1)

        # TODO: might want to double check that the current option is valid
        #       in case of user manually changing it in the config.ini

        # NOTE: media/user_metadata.json will store only the metadata of all
        # the users

        # NOTE: Case: We are in debug mode
        #   myreddit-dl/debug_dir

        # NOTE: Case: NOT path given or given path is NOT valid.
        #   $HOME/Pictures/reddit_user/ ...

        # NOTE: Case: Given path is valid
        #   $PATH/reddit_user/ ...


#    def _parse_path(self) -> str:
#        if self.arg_dict['debug']:
#            return os.getcwd() + os.sep + 'test_media' + os.sep
#
#        given_path = self.config['PATH']['path']
#
#        # no path given. Default to $HOME/Pictures
#        if len(given_path) == 0:
#            if os.path.isdir(self.DEFAULT_DIR):
#                return self.DEFAULT_DIR
#        else:
#            if os.path.isdir(given_path):
#                return given_path
#            else:
