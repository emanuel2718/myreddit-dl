import configparser
import os
import utils


class ConfigHandler:
    def __init__(self, config_path: str) -> None:
        self.log = utils.setup_logger(__name__)
        self.config_path = config_path
        self.conf = configparser.ConfigParser()
        self.conf.read(self.config_path)

    def __getitem__(self):
        return self.config

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

    @property
    def fmt(self):
        return ('{}\n'
                '{:8} = {}\n'
                '{:8} = {}\n'
                '{:8} = {}\n')

    @property
    def config(self):
        return self.conf

    def write_config(self, section: str, key: str, value: str) -> None:
        self.config.set(section, key, value)

        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

    def get_default_media_path(self) -> str:
        pictures = os.path.expanduser(f'~{os.sep}Pictures{os.sep}')
        return pictures + self.get_client_username() + '_reddit' + os.sep

    def set_media_path(self, path: str) -> None:
        self.log.info(f'Setting path: {path}')
        self.write_config('DEFAULTS', 'path', path)

    def get_client_username(self) -> str:
        ''' Reddit client username'''
        return self.config.get('USERS', 'current_user_section_name')

    def get_prefix(self) -> str:
        ''' Currently set prefix option'''
        return self.config.get('DEFAULTS', 'prefix')

    def get_media_path(self):
        return self.config.get('DEFAULTS', 'path')

    def get_valid_prefix_options(self) -> set:
        # NOTE: this used to return a str
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
            self.write_config('DEFAULTS', 'prefix', prefix)
            self.log.info(f'Prefix changed to: {prefix}')

        else:
            self.log.error(utils.INVALID_CFG_OPTION_MESSAGE)





if __name__ == '__main__':
    # TODO: change this message
    print('dont run this.')
