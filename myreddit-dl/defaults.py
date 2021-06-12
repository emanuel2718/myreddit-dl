import pathlib
import utils
import configparser
import os
from platform import system

# TODO: Make this have the args...
# TODO: Refactor this whole entire file.

class Defaults:
    def __init__(self, debug=False) -> None:
        self.log = utils.setup_logger(__name__, True)
        self.debug = debug
        #self.log.debug('THIS HAPPENS Defaults().__init__()')

    @property
    def config(self):
        config = configparser.ConfigParser()
        config.read(utils.CFG_FILENAME)
        return config
        #return configparser.ConfigParser().read(utils.CFG_FILENAME)

    @property
    def home_dir(self) -> str:
        return os.path.expanduser('~')

    @property
    def project_dir(self) -> str:
        return utils.PROJECT_DIR

    @property
    def user_section_name(self) -> str:
        '''
        Returns the current user config [SECTION] name

        @return: str: current user section name.
        '''
        return str(self.config['USERS']['current_user_section_name'])

    @property
    def username(self) -> str:
        return str(self.config[self.user_section_name]['username'])

    @property
    def media_folder(self) -> str:
        return str(self.project_dir + 'media' + os.sep)

    @property
    def default_config_path(self) -> str:
        return str(self.home_dir + os.sep + 'Pictures' + os.sep +
                   self.username + '_reddit' + os.sep)


    def __write_config(self, section: str, key: str, value: str) -> None:
        self.config.set(section, key, value)
        with open(utils.CFG_FILENAME, 'w') as config:
            self.config.write(config)

    def set_path_to_default(self) -> None:
        default_path = self.default_config_path
        self.__write_config(f'DEFAULTS', 'path', default_path)
        self.log.info(f'Path set to myreddit-dl default path: {default_path}')

    def set_config_prefix(self, prefix: list) -> None:
        valid_options = utils.get_valid_prefix_options()
        given = '_'.join(prefix).lower()

        if given not in valid_options:
            self.log.error(utils.INVALID_CFG_OPTION_MESSAGE)
            return
        if given == self.config['DEFAULTS']['prefix']:
            self.log.info('This is already the current set prefix option.')
            return

        # Different valid option given (username or subreddit)
        try:
            self.__write_config('DEFAULTS', 'prefix', given)
            self.log.info(f'Prefix format changed to: {given}')

        except BaseException:
            self.log.error('Something went wrong changing the prefix format')
            exit(1)

    def set_base_path(self, path: str) -> None:
        sanitized_path = self._sanitize_path(path)
        if os.path.exists(sanitized_path) or sanitized_path is not None:
            self.__write_config('DEFAULTS', 'path', sanitized_path)
            self.log.info(f'Path set to: {sanitized_path}')
            return

    def _sanitize_path(self, path: str) -> str or None:
        # TODO: I don't like this. Refactor this.
        if path.startswith(self.home_dir):
            pass
        # user forgot /home/user and typed home/user
        elif path.startswith(self.home_dir.lstrip(os.sep)):
            path = self.home_dir + path[len(self.home_dir) - 1:]
        elif path.startswith('~/'):
            path = self.home_dir + os.sep + path[1:]
        elif path.startswith('$HOME/'):
            path = self.home_dir + os.sep + path[6:]
        elif path.startswith('./'):
            path = os.getcwd() + path[1:]
        elif path.startswith('/'):
            path = path
        else:
            path = self.home_dir + os.sep + path

        path = path if path.endswith(os.sep) else path + os.sep

        if system() == 'Windows':
            path = path.replace('/', '\\')

        if self.is_valid_path(path):
            return path
        return self.default_config_path


    def get_metadata_file(self) -> str:
        return self.media_folder + self.username + '_metadata.json'

    def get_file_prefix(self) -> str:
        return str(self.config['DEFAULTS']['prefix'])

    def get_base_path(self, clean=False) -> str:
        if self.debug or clean:
            self.log.debug(
                f"get_base_path() ->"
                f"{str(utils.PROJECT_PARENT_DIR + 'debug_media' + os.sep)}")
            return str(utils.PROJECT_PARENT_DIR + 'debug_media' + os.sep)

        if len(self.config['DEFAULTS']['path']) != 0:
            config_path = str(self.config['DEFAULTS']['path'])
            if self.is_valid_path(config_path):
                return config_path

        self.set_path_to_default()
        return self.default_config_path

    def is_valid_path(self, path: str) -> bool:
        return True if os.path.isabs(path) else False

    def clean_debug(self):
        import shutil
        debug_path = self.get_base_path(True)
        try:
            shutil.rmtree(debug_path)
            self.log.info(f'Removed debug folder: {debug_path}')
        except BaseException:
            self.log.info(f'Debug folder not found.')
