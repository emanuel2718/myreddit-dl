import configparser
import getpass
import myredditdl.utils as utils
from myredditdl.config_handler import ConfigHandler
from myredditdl.reddit_client import RedditClient

class Cli:
    def __init__(self):
        self.log = utils.setup_logger(__name__)
        self.config = ConfigHandler()

    def display_setup_header(self) -> None:
        instructions = utils.DEVELOPER_APP_INSTRUCTIONS
        header = '-' * 20 + ' SETUP CONFIGURATOR ' + '-' * 20
        print('\n' + header)
        print(
            'For information'
            ' on how to setup your own developer credentials to use myredditdl,\n'
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

    def client_setup(self, request=None) -> None:
        ''' Sets up new Reddit client if the given credentials are valid
            Reddit instances. If valid, then go ahead an add the client.
            If invalid; exit the program.
        '''
        self.display_setup_header()
        new_client_instance = self.new_client_prompt()

        if RedditClient.validate_instance(new_client_instance):
            self.config.add_client(new_client_instance)
        else:
            self.log.warning('Invalid reddit instance provided')
            exit(0)

    def change_client_prompt(self, options: dict) -> None:
        print('\n Valid Reddit Clients:\n')
        for k, v in options.items():
            print(f'{k}. {v}')

        res = ''
        while res not in options.keys():
            res = input('\nPlease, chose a client to change to: ')

        if res == str(len(options)):
            self.log.info('Thank you for using myredditdl')
            exit(0)
        self.config.set_new_current_user(options.get(res))

    def get_clients_options(self) -> dict:
        clients = self.config.get_available_reddit_clients()
        clients.append('Exit program')
        return {str(index):client for index, client in enumerate(clients, 1)}

    def change_client(self, request=None):
        options = self.get_clients_options()
        self.change_client_prompt(options)

    def change_path(self, request: str):
        self.config.set_media_path(request)

    def change_prefix(self, request: list):
        self.config.set_prefix_option('_'.join(request))


#    def _prompt_user_change(self, username: str) -> str:
#        res = ''
#        while res not in {'y', 'yes', 'n', 'no'}:
#            res = input(
#                f'\nINFO: {username} is not currently set as the default client.\n'
#                f'\nWould you like to set {username} as default client?'
#                ' (y)es, (n)o: ').lower()
#        return res
#
