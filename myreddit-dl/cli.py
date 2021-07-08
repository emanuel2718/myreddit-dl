import configparser
import getpass
import utils
from config_handler import ConfigHandler
from reddit_client import RedditClient

class Cli:
    def __init__(self):
        self.log = utils.setup_logger(__name__)
        self.config = ConfigHandler()
        self.client = RedditClient()

    def display_setup_header(self) -> None:
        instructions = utils.DEVELOPER_APP_INSTRUCTIONS
        header = '-' * 20 + ' SETUP CONFIGURATOR ' + '-' * 20
        print('\n' + header)
        print(
            'For information'
            ' on how to setup your own developer credentials to use myreddit-dl,\n'
            'Please refer to',
            instructions)

        print(
            '\nInput your reddit developer credentials below. Make sure they are correct.')
        print('-' * len(header))

    def new_client_prompt(self) -> dict:
        ''' Prompts the user for new client information and returns the
            information as a dictionary.
        '''
        client_id = input('1. Client Id: ').strip(' ')
        client_secret = input('2. Client secret: ').strip(' ')
        username = input('3. Username: ').strip(' ')
        password = input('4. Password: ').strip(' ')
        print('\n')

        return {'section': username.upper(),
                'client_id': client_id,
                'client_secret': client_secret,
                'username': username,
                'password': password}

    def client_setup(self) -> None:
        ''' Sets up new Reddit client if the given credentials are valid
            Reddit instances. If valid, then go ahead an add the client.
            If invalid; exit the program.
        '''
        self.display_setup_header()
        new_client_instance = self.new_client_prompt()

        if self.client.validate_instance(new_client_instance):
            self.config.add_client(instance)
        else:
            self.log.warning('Invalid reddit instance provided')
            exit(0)

    def change_client(self):
        pass

    def show_config(self):
        pass

    def change_path(self):
        pass

    def change_prefix(self):
        pass



#
#    def change_client(self):
#        invalid_sections = {'DEFAULTS', 'USERS', 'REDDIT'}
#        sections = [sec for sec in self.config.sections()
#                    if sec not in invalid_sections]
#        options = {}
#        res = ''
#        print('\nValid Reddit clients:\n')
#        for i, section in enumerate(sections, 1):
#            print(f'{i}. {self.config[section]["username"]}')
#            options[str(i)] = self.config[section]['username']
#        options[str(len(sections) + 1)] = 'Exit'
#        print(f'{len(sections)+1}. Exit Program')
#
#        while res not in list(options.keys()):
#            res = input('\nPlease chose the client you want to change to: ')
#
#        if res == str(len(sections) + 1):
#            exit(0)
#
#        if self.config['USERS']['current_user_section_name'] == options[res].upper():
#            self.log.info(
#                f'{options[res]} is already the current reddit client.')
#            exit(0)
#
#        self.config['USERS']['current_user_section_name'] = options[res].upper()
#        with open(utils.CFG_FILENAME, 'w') as config_file:
#            self.config.write(config_file)
#            self.log.info(f'Reddit client changed to {options[res]}')
#
#    def _prompt_user_change(self, username: str) -> str:
#        res = ''
#        while res not in {'y', 'yes', 'n', 'no'}:
#            res = input(
#                f'\nINFO: {username} is not currently set as the default client.\n'
#                f'\nWould you like to set {username} as default client?'
#                ' (y)es, (n)o: ').lower()
#        return res
#
#    def _config_setup_header(self):
#        instructions = utils.DEVELOPER_APP_INSTRUCTIONS
#        header = '-' * 20 + ' SETUP CONFIGURATOR ' + '-' * 20
#        print('\n' + header)
#        print(
#            'For information'
#            ' on how to setup your own developer credentials to use myreddit-dl,\n'
#            'Please refer to',
#            instructions)
#
#        print(
#            '\nInput your reddit developer credentials below. Make sure they are correct.\n')
#        print('-' * len(header))
#
#    def prompt_client_config_setup(self, hidden_password=False):
#        print()
#        utils.print_warning(
#            'Either this is your first time using myreddit-dl'
#            ' or there appear to be a problem in your reddit app'
#            ' client information.\n\n')
#        response = ''
#        while response not in {'y', 'yes', 'n', 'no'}:
#            response = input('Would you like to fix it? (y)es, (n)o: ').lower()
#
#        if response == 'n' or response == 'no':
#            exit(0)
#        return self.client_config_setup(hidden_password)
#
#    def print_config_data(self, show_password=False):
#        print('Current Configuration:')
#
#        for section in self.config.sections():
#            print(f'\n\n[{section}]')
#            for (key, val) in dict(self.config[section]).items():
#                if key == 'password':
#                    if show_password:
#                        print(f'{key.upper()} = {val}')
#                    else:
#                        continue
#                else:
#                    print(f'{key.upper()} = {val}')
