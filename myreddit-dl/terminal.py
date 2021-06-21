import configparser
import getpass
import utils


class Terminal:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(utils.CFG_FILENAME)
        self.log = utils.setup_logger(__name__, False)

    def client_config_setup(self, hidden_password=False):
        self._config_setup_header()
        client_id = input('1. Client Id: ').strip(' ')
        client_secret = input('2. Client Secret: ').strip(' ')
        username = input('3. Username: ').strip(' ')

        if hidden_password:
            password = getpass.getpass('4. Password (hidden): ').strip(' ')
        else:
            password = input('4. Password: ').strip(' ')

        section_name = username.upper()
        if not self.config.has_section(section_name):
            self.config.add_section(section_name)


        self.config.set(section_name, 'client_id', client_id)
        self.config.set(section_name, 'client_secret', client_secret)
        self.config.set(section_name, 'username', username)
        self.config.set(section_name, 'password', password)

        if len(self.config['USERS']['current_user_section_name']) == 0:
            self.config['USERS']['current_user_section_name'] = section_name
            self.log.info(f'{username} added as default client.')

        elif self.config['USERS']['current_user_section_name'] != section_name:
            response = self._prompt_user_change(username)
            if response == 'y' or response == 'yes':
                self.config['USERS']['current_user_section_name'] = section_name
                self.log.info(f'{username} set as default client.')
            else:
                self.log.info(f"{self.config['USERS']['current_user_section_name']} "
                      "left as default client.")


        with open(utils.CFG_FILENAME, 'w') as config_file:
            self.config.write(config_file)
            self.log.info('Reddit developer app updated succesfully.\n')

        return

    def change_client(self):
        invalid_sections = {'DEFAULTS', 'USERS', 'REDDIT'}
        sections = [sec for sec in self.config.sections() if sec not in invalid_sections]
        options = {}
        res = ''
        print('\nValid Reddit clients:\n')
        for i, section in enumerate(sections, 1):
            print(f'{i}. {self.config[section]["username"]}')
            options[str(i)] = self.config[section]['username']
        options[str(len(sections)+1)] = 'Exit'
        print(f'{len(sections)+1}. Exit Program')


        while res not in list(options.keys()):
            res = input('\nPlease chose the client you want to change to: ')

        if res == str(len(sections) + 1):
            exit(0)

        if self.config['USERS']['current_user_section_name'] == options[res].upper():
            self.log.info(f'{options[res]} is already the current reddit client.')
            exit(0)


        self.config['USERS']['current_user_section_name'] = options[res].upper()
        with open(utils.CFG_FILENAME, 'w') as config_file:
            self.config.write(config_file)
            self.log.info(f'Reddit client changed to {options[res]}')


    def _prompt_user_change(self, username: str) -> str:
        res = ''
        while res not in {'y', 'yes', 'n', 'no'}:
            res = input(f'\nINFO: {username} is not currently set as the default client.\n'
                        f'\nWould you like to set {username} as default client?'
                        ' (y)es, (n)o: ').lower()
        return res

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

    def prompt_client_config_setup(self, hidden_password=False):
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
        return self.client_config_setup(hidden_password)

    def print_config_data(self, show_password=False):
        print('Current Configuration:')

        for section in self.config.sections():
            print(f'\n\n[{section}]')
            for (key, val) in dict(self.config[section]).items():
                if key == 'password':
                    if show_password:
                        print(f'{key.upper()} = {val}')
                    else:
                        continue
                else:
                    print(f'{key.upper()} = {val}')
