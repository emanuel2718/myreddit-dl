import pathlib
import utils
import configparser
import os


class Defaults:
    def __init__(self, debug=False) -> None:
        self.debug = debug
        self.config = configparser.ConfigParser()
        self.HOME_DIR = os.path.expanduser('~')
        self.PROJECT_DIR = utils.PROJECT_DIR

    def __write_config(self, section: str, key: str, value: str) -> None:
        self.config.set(section, key, value)
        with open(utils.CFG_FILENAME, 'w') as config_file:
            self.config.write(config_file)

    def set_path_to_default(self, username: str) -> None:
        default_path = f'{self.HOME_DIR}/Pictures/{username}_media/'
        self.config.read(utils.CFG_FILENAME)
        self.__write_config(f'DEFAULT', 'path', default_path)
        utils.print_info(f'Path set to default: {default_path}')


    def set_config_save(self, save_as: str) -> None:
        save_as = save_as.lower()
        if save_as != utils.CFG_SAVE_DEFAULT and save_as != 'username':
            utils.print_error(utils.INVALID_CFG_OPTION)
            return

        self.config.read(utils.CFG_FILENAME)
        if save_as == self.config['DEFAULT']['filename_save']:
            utils.print_info('This is already the current set saving option.')
            return

        # Different valid option given (username or subreddit)
        try:
            self.__write_config('DEFAULT', 'filename_save', save_as)
            utils.print_info(f'Save format changed to: {save_as}')

        except BaseException:
            utils.print_error(
                'Something went wrong changing the saving format.')
            exit(1)

    def set_base_path(self, path: str) -> None:
        self.config.read(utils.CFG_FILENAME)
        if os.path.exists(path):
            self.__write_config('DEFAULT', 'path', path)
            utils.print_info(f'Path set to: {path}')
            return

        sanitized_path = self._sanitize_path(path)

        if sanitized_path is not None:
            self.__write_config('DEFAULT', 'path', path)
            utils.print_info(f'Path set to: {path}')


    def _sanitize_path(self, path: str) -> str or None:
        if path.startswith('~/'):
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

        if os.path.isabs(path):
            return path
        return None # not valid path

    @property
    def media_folder(self) -> str:
        return str(self.PROJECT_DIR + 'media' + os.sep)


    def get_metadata_file(self, username: str) -> str:
        return self.media_folder + username + '_metadata.json'

    def get_file_prefix(self) -> str:
        self.config.read(utils.CFG_FILENAME)
        return str(self.config['DEFAULT']['filename_save'])

    def get_base_path(self) -> str:
        if self.debug:
            return str(utils.PROJECT_PARENT_DIR + 'debug_media' + os.sep)

        self.config.read(utils.CFG_FILENAME)
        return str(self.config['DEFAULT']['path'])
