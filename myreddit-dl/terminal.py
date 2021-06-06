import configparser
import getpass
import utils


class Terminal:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(utils.CFG_FILENAME)

    def client_config_setup(self):
        self._config_setup_header()
        client_id = input('1. Client Id: ').strip(' ')
        client_secret = input('2. Client Secret: ').strip(' ')
        username = input('3. Username: ').strip(' ')
        password = getpass.getpass('4. Password (hidden): ').strip(' ')

        self.config.set('REDDIT', 'client_id', client_id)
        self.config.set('REDDIT', 'client_secret', client_secret)
        self.config.set('REDDIT', 'username', username)
        self.config.set('REDDIT', 'password', password)

        with open(utils.CFG_FILENAME, 'w') as config_file:
            self.config.write(config_file)
            print('\nReddit developer app updated succesfully.\n')
        return

    def _config_setup_header(self):
        instructions = utils.DEVELOPER_APP_INSTRUCTIONS
        header = '-' * 20 + ' SETUP CONFIGURATOR ' + '-' * 20
        print('\n' + header)
        print(
            'For information'
            ' on how to setup your own developer credentials to use myreddit-dl,\n'
            'Please refer to',
            instructions)

        print(
            '\nInput your reddit developer credentials below. Make sure they are correct.\n')
        print('-' * len(header))

    def prompt_client_config_setup(self):
        print()
        utils.print_warning(
            'Either this is your first time using myreddit-dl'
            ' or there appear to be a problem in your reddit app'
            ' client information.\n\n')
        response = ''
        while response not in {'y', 'yes', 'n', 'no'}:
            response = input('Would you like to fix it? (y)es, (n)o: ').lower()

        if response == 'n' or response == 'no':
            exit(0)
        return self.client_config_setup()

    def print_config_data(self, show_password=False):
        print('Current Configuration:')

        print('\n[DEFAULT]\n')
        print('Prefix:', self.config['DEFAULT']['filename_prefix'])
        print('Path:', self.config['DEFAULT']['path'])

        print('\n[REDDIT]\n')
        print('Client Id:', self.config['REDDIT']['client_id'])
        print('Client Secret:', self.config['REDDIT']['client_secret'])
        print('Username:', self.config['REDDIT']['username'])
        if show_password:
            print('Password:', self.config['REDDIT']['password'])
