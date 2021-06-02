#import configparser
#import os


#class Defaults:
#    def __init__(self, debug=False) -> None:
#
#        # NOTE: media/user_metadata.json will store only the metadata of all the users
#
#        # NOTE: Case: We are in debug mode
#        #   myreddit-dl/debug_dir
#
#        # NOTE: Case: NOT path given or given path is NOT valid.
#        #   $HOME/Pictures/reddit_user/ ...
#
#        # NOTE: Case: Given path is valid
#        #   $PATH/reddit_user/ ...
#
#        self.config = configparser.ConfigParser()
#        self.config.read('config.ini')
#        self.HOME_DIR = os.path.expanduser('~')
#        self.DEFAULT_DIR = self.HOME_DIR + os.sep + 'Pictures'
#        self.BASE_PATH = self._parse_path()
#
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
