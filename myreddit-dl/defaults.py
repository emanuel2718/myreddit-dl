import pathlib
import utils
import configparser
import os
from platform import system

# TODO: Make this have the args...


class Defaults:
    def __init__(self, debug=False) -> None:
        self.log = utils.setup_logger(__name__, debug)
        self.conf = configparser.ConfigParser()
        self.conf.read(self._config_filepath)

    @property
    def config(self):
        return self.conf

    @property
    def _config_filepath(self) -> str:
        return self.project_dir + 'config.ini'

    @property
    def project_parent_dir(self) -> str:
        return str(pathlib.Path(__file__).parent.parent) + os.sep

    @property
    def project_dir(self) -> str:
        return str(pathlib.Path(__file__).parent) + os.sep

    @property
    def media_folder(self) -> str:
        return str(self.project_dir + 'media' + os.sep)

    @property
    def home_dir(self) -> str:
        return str(os.path.expanduser('~'))

    @property
    def client_username(self) -> str:
        ''' Current Reddit client username'''
        return str(self.config[self.config_section_name]['username'])

    @property
    def config_section_name(self) -> str:
        ''' Returns the current user config [SECTION] name '''
        return str(self.config['USERS']['current_user_section_name'])

    @property
    def config_prefix(self) -> str:
        return self.config['DEFAULTS']['prefix']

    @property
    def config_media_path(self) -> str:
        return str(self.config['DEFAULTS']['path'])

    @property
    def debug_path(self) -> str:
        return str(self.project_parent_dir + 'debug_media' + os.sep)

    @property
    def metadata_file(self) -> str:
        ''' Returns the full path of the metadata file'''
        return self.media_folder + self.client_username + '_metadata.json'

    def __write_config(self, section: str, key: str, value: str) -> None:
        self.config.set(section, key, value)
        with open(self._config_filepath, 'w') as configfile:
            self.config.write(configfile)

    def __get_default_config_media_path(self) -> str:
        return str(self.home_dir + os.sep + 'Pictures' + os.sep +
                   self.client_username + '_reddit' + os.sep)

    def __get_valid_config_prefix_options(self) -> str:
        return (
            'subreddit',
            'username',
            'subreddit_username',
            'username_subreddit')

    def set_default_config_media_path(self) -> None:
        default_path = self.__get_default_config_media_path()
        self.__write_config('DEFAULTS', 'path', default_path)
        self.log.info(f'Path set to default path: {default_path}')

    def set_config_prefix(self, prefix: list) -> None:
        # TODO: Make this smarter to be more expansive in the future
        #       __get_valid_config_prefix_options() needs to be changed
        #       Example: The user want the prefix to be title_username or
        #                tags_subreddit or something crazy like
        #                tags_subreddit_title_username (for whatever reason...)
        valid_options = self.__get_valid_config_prefix_options()
        given = '_'.join(prefix).lower()

        if given == self.config_prefix:
            self.log.info(f'{given} is already the current prefix option.')
            return

        if given in valid_options:
            self.__write_config('DEFAULTS', 'prefix', given)
            self.log.info(f'Prefix format changed to: {given}')
            return

        self.log.error(utils.INVALID_CFG_OPTION_MESSAGE)

    def set_media_path(self, path: str) -> None:
        sanitized_path = self.__sanitize_path(path)
        if os.path.exists(sanitized_path) or sanitized_path is not None:
            self.__write_config('DEFAULTS', 'path', sanitized_path)
            self.log.info(f'Path set to: {sanitized_path}')
            return
        self.set_default_config_media_path()

    def __is_valid_path(self, path: str) -> bool:
        return True if os.path.isabs(path) else False

    def __sanitize_path(self, path: str) -> str or None:
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

        if self.__is_valid_path(path):
            return path
        return self.default_config_path

    def clean_debug(self):
        import shutil
        path = self.debug_path
        try:
            os.remove('debug_log')
            self.log.info(f'Removed debug_log')

        except FileNotFoundError:
            self.log.error('debug_log not found')
        try:
            shutil.rmtree(path)
            self.log.info(f'Removed debug folder: {path}')

        except FileNotFoundError:
            self.log.info(f'Debug folder not found.')
