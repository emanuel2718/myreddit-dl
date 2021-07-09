import configparser
import utils
import sys, errno, os
from pathlib import Path, PosixPath, PurePath, PurePosixPath


class ConfigHandler:
    def __init__(self) -> None:
        self.log = utils.setup_logger(__name__)
        self.config_path = utils.CFG_FILENAME
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

    def __getitem__(self):
        return self.conf

    def __repr__(self):
        return 'Config(user=%r, prefix=%r, path=%r)' % (
            self.get_client_username(),
            self.get_prefix(),
            self.get_media_path())

    def __str__(self) -> str:
        return self.fmt.format('Configuration:\n',
                               'Username', self.get_client_username(),
                               'Prefix', self.get_prefix(),
                               'Path', self.get_media_path())

    def __print__(self, request=None) -> None:
        print(self.__str__())

    @property
    def fmt(self):
        return ('{}\n'
                '{:8} = {}\n'
                '{:8} = {}\n'
                '{:8} = {}\n')

    def get_config(self):
        return self.config

    def get_available_reddit_clients(self) -> list:
        return [sec for sec in self.config.sections()
                if sec not in ('DEFAULTS', 'USERS', 'REDDIT')]

    def set_new_current_user(self, section_name: str) -> None:
        ''' Section name is the current reddit client username in Upper case
            which points to the current user section name in the config file.

            Example:
            ['USERS'] -> this are section names
            current_user_section_name = RANDOM_USERNAME

            [RANDOM_USERNAME] -> this are section names
            client_id=
            client_secret=
            etc...

            Now random_username will be the new active reddit client
        '''
        self.config.set('USERS', 'current_user_section_name', section_name)
        self.write_config()
        self.log.info(f'Successfully changed to user: {section_name}')

    def add_client(self, client: dict) -> None:
        ''' Receives a client in the form of:

            {section: section name,
             id: client_id,
             secret: client_secret,
             username: username,
             password: password,
            }

        '''
        section = client.get('section')
        if not self.config.has_section(section):
            self.config.add_section(section)
            self.config.set(section, 'client_id', client.get('client_id'))
            self.config.set(section, 'client_secret',client.get('client_secret'))
            self.config.set(section, 'username', client.get('username'))
            self.config.set(section, 'password', client.get('password'))
            self.write_config()
            self.log.info(
                f"{client.get('username')} successfully added as a client")

        else:
            self.log.info('That client already exists.')

    def write_config(self) -> bool:
        try:
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
                return True

        except FileNotFoundError:
            self.log.debug('Write config failed!')
            return False

    def get_default_media_path(self) -> str:
        ''' Returns the location of the user ~/Pictures/{reddit_username}_reddit/
            media folder
        '''
        pictures = os.path.expanduser(f'~{os.sep}Pictures{os.sep}')
        return pictures + self.get_client_username() + '_reddit' + os.sep


    def get_client_username(self) -> str:
        ''' Reddit client username'''
        return self.config.get('USERS', 'current_user_section_name')

    def get_prefix(self) -> str:
        ''' Currently set prefix option'''
        return self.config.get('DEFAULTS', 'prefix')

    def get_media_path(self):
        return self.config.get('DEFAULTS', 'path')

    def get_valid_prefix_options(self) -> set:
        return {'subreddit',
                'username',
                'subreddit_username',
                'username_subreddit'}

    def set_prefix_option(self, prefix: str) -> None:
        ''' Receives a prefix option in the form of a string:
            Example: subreddit_username
            Example: username

            Note: see @get_valid_prefix_options() for valid prefixes
        '''
        if prefix == self.get_prefix():
            self.log.info(f'{prefix} is already the current prefix option')

        elif prefix in self.get_valid_prefix_options():
            self.config.set('DEFAULTS', 'prefix', prefix)
            self.write_config()
            self.log.info(f'Prefix changed to: {prefix}')

        else:
            self.log.error(utils.INVALID_CFG_OPTION_MESSAGE)

    def set_media_path(self, path: str) -> None:
        ''' Changes the destination folder for downloaded media
            to @path
        '''
        if path.lower() == 'default':
            path = self.get_default_media_path()

        elif self.is_path_creatable_or_exists(path):
            path = self.sanitize_path(path)
        else:
            self.log.info(f"cannot create directory '{path}': No such file or directory")
            return

        self.config.set('DEFAULTS', 'path', path)
        self.write_config()
        self.log.info(f'media path set to: {path}')

    def sanitize_path(self, path: str) -> str:
        ''' Cleans up given @path from --path flag
            This function attempts to handle relative paths but definetly needs
            further testing.
        '''
        root = Path.home() if path.startswith(str(Path.home())) else Path.cwd()
        parts = PosixPath(path).parts
        for part in parts:
            if part == '..':
                root = root.parent

        return str(root) + ''.join([os.sep + p for p in parts
                                    if p != '..'
                                    and p != os.sep
                                    and p not in str(root).split(os.sep)])


    # Credits to: stackoverflow.com/questions/9532499
    def is_path_creatable_or_exists(self, path: str) -> bool:

        try:
            return self.is_path_valid(path) and (
                os.path.exists(path) or self.is_path_creatable(path))

        except OSError:
            return False

    def is_path_creatable(self, path: str) -> bool:
        dirname = os.path.dirname(path) or os.getcwd()
        return os.access(dirname, os.W_OK)


    def is_path_valid(self, path: str) -> bool:
        try:
            if not isinstance(path, str) or not path:
                return False

            _, path = os.path.splitdrive(path)

            root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
                if sys.platform == 'win32' else os.path.sep
            assert os.path.isdir(root_dirname)

            root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

            for pathname_part in path.split(os.path.sep):
                try:
                    os.lstat(root_dirname + pathname_part)

                except OSError as exc:
                    if hasattr(exc, 'winerror'):
                        if exc.winerror == utils.ERROR_INVALID_NAME:
                            return False
                    elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                        return False

        except TypeError as exc:
            return False
        else:
            return True

if __name__ == '__main__':
    # TODO: change this message
    print('dont run this.')
