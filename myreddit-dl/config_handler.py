import configparser


class ConfigHandler:
    def __init__(self, config_path: str) -> None:
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
    def __config_filepath(self):
        return self.src_dir

    @property
    def config(self):
        return self.conf

    def get_client_username(self) -> str:
        ''' Reddit client username'''
        return self.config.get('USERS', 'current_user_section_name')

    def get_prefix(self) -> str:
        ''' Currently set prefix option'''
        return self.config.get('DEFAULTS', 'prefix')

    def get_media_path(self):
        return self.config.get('DEFAULTS', 'path')

    def write_config(self, section: str, key: str, value: str) -> None:
        self.config.set(section, key, value)

        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)




if __name__ == '__main__':
    # TODO: change this message
    print('dont run this.')
