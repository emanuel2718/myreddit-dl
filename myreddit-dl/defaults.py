import pathlib
import utils
import configparser
import os
from platform import system


class Defaults:
    def __init__(self, debug=False) -> None:
        self.log = utils.setup_logger(__name__, True)
        self.debug = debug
        self.config = configparser.ConfigParser()
        self.config.read(utils.CFG_FILENAME)
        self.HOME_DIR = os.path.expanduser('~')
        self.PROJECT_DIR = utils.PROJECT_DIR
        self.USERNAME = str(self.config['REDDIT']['username'])

    def __write_config(self, section: str, key: str, value: str) -> None:
        self.config.set(section, key, value)
        with open(utils.CFG_FILENAME, 'w') as config_file:
            self.config.write(config_file)

    def set_path_to_default(self) -> None:
        default_path = self.default_config_path
        self.__write_config(f'DEFAULT', 'path', default_path)
        self.log.info(f'Path set to myreddit-dl default path: {default_path}')

    def set_config_prefix(self, prefix: list) -> None:
        valid_options = utils.get_valid_prefix_options()
        given = '_'.join(prefix).lower()

        if given not in valid_options:
            self.log.error(utils.INVALID_CFG_OPTION_MESSAGE)
            return
        if given == self.config['DEFAULT']['filename_prefix']:
            self.log.info('This is already the current set prefix option.')
            return

        # Different valid option given (username or subreddit)
        try:
            self.__write_config('DEFAULT', 'filename_prefix', given)
            self.log.info(f'Prefix format changed to: {given}')

        except BaseException:
            self.log.error('Something went wrong changing the prefix format')
            exit(1)

    def set_base_path(self, path: str) -> None:
        sanitized_path = self._sanitize_path(path)
        if os.path.exists(sanitized_path) or sanitized_path is not None:
            self.__write_config('DEFAULT', 'path', sanitized_path)
            self.log.info(f'Path set to: {sanitized_path}')
            return

    def _sanitize_path(self, path: str) -> str or None:
        # TODO: I don't like this. Refactor this.
        if path.startswith(self.HOME_DIR):
            pass
        # user forgot /home/user and typed home/user
        elif path.startswith(self.HOME_DIR.lstrip(os.sep)):
            path = self.HOME_DIR + path[len(self.HOME_DIR) - 1:]
        elif path.startswith('~/'):
            path = self.HOME_DIR + os.sep + path[1:]
        elif path.startswith('$HOME/'):
            path = self.HOME_DIR + os.sep + path[6:]
        elif path.startswith('./'):
            path = os.getcwd() + path[1:]
        elif path.startswith('/'):
            path = path
        else:
            path = self.HOME_DIR + os.sep + path

        path = path if path.endswith(os.sep) else path + os.sep

        if system() == 'Windows':
            path = path.replace('/', '\\')

        if self.is_valid_path(path):
            return path
        return self.default_config_path

    @property
    def media_folder(self) -> str:
        return str(self.PROJECT_DIR + 'media' + os.sep)

    @property
    def default_config_path(self) -> str:
        return str(self.HOME_DIR + os.sep + 'Pictures' + os.sep +
                   self.USERNAME + '_reddit' + os.sep)

    def get_metadata_file(self) -> str:
        return self.media_folder + self.USERNAME + '_metadata.json'

    def get_file_prefix(self) -> str:
        return str(self.config['DEFAULT']['filename_prefix'])

    def get_base_path(self, clean=False) -> str:
        if self.debug or clean:
            self.log.debug(
                f"get_base_path() ->"
                f"{str(utils.PROJECT_PARENT_DIR + 'debug_media' + os.sep)}")
            return str(utils.PROJECT_PARENT_DIR + 'debug_media' + os.sep)

        config_path = str(self.config['DEFAULT']['path'])
        if self.is_valid_path(config_path):
            return config_path

        self.set_path_to_default()
        return self.default_config_path

    def is_valid_path(self, path: str) -> bool:
        return True if os.path.isabs(path) else False

    def clean_debug(self):
        import shutil
        debug_path = self.get_base_path(True)
        shutil.rmtree(debug_path)
        self.log.debug(f'Removed debug folder: {debug_path}')
