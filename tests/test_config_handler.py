import configparser
import logging
import unittest
from os import sep
from os.path import expanduser
from myredditdl.config_handler import ConfigHandler
from unittest import mock
from unittest.mock import patch


class TestConfigHandler(unittest.TestCase):
    MOCK_CFG = '''
    [DEFAULTS]
    prefix = subreddit_username
    path =

    [USERS]
    current_user_section_name = MOCK_CLIENT

    [MOCK_CLIENT]
    client_id = mock_id
    client_secret = mock_secret
    username = mock_username
    password = mock_password
    '''

    VALID_OPTIONS = {'subreddit',
                     'username',
                     'subreddit_username',
                     'username_subreddit'}

    def setUp(self):
        self.cfg = ConfigHandler()
        self.config = configparser.RawConfigParser()
        self.config.read_string(self.MOCK_CFG)
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_available_reddit_clients(self):
        sections = ['DEFAULTS', 'USERS', 'EMPTY_CLIENT', 'FIRST', 'SECOND']
        with patch.object(ConfigHandler, 'get_config_sections', return_value=sections):
            self.assertEqual(
                self.cfg.get_available_reddit_clients(), [
                    'FIRST', 'SECOND'])

    def test_set_new_current_user(self):
        with patch.object(ConfigHandler, 'get_client_active_section', return_value='RANDOM_USER'):
            self.assertFalse(self.cfg.set_new_current_user('RANDOM_USER'))
            self.assertTrue(self.cfg.set_new_current_user('new_user'))

    @mock.patch('myredditdl.config_handler.ConfigHandler.get_valid_prefix_options')
    @mock.patch('myredditdl.config_handler.ConfigHandler.get_prefix')
    def test_set_prefix_option(self, mock_prefix, mock_options):
        mock_prefix.return_value = 'subreddit_name'
        mock_options.return_value = self.VALID_OPTIONS
        self.assertFalse(self.cfg.set_prefix_option('subreddit_name'))
        self.assertTrue(self.cfg.set_prefix_option('username'))
        self.assertTrue(self.cfg.set_prefix_option('username_subreddit'))
        self.assertFalse(self.cfg.set_prefix_option('sub_name'))

    def test_default_media_path(self):
        home = expanduser('~/Pictures/')
        with patch.object(ConfigHandler, 'get_client_active_section', return_value='SATORU'):
            self.assertEqual(
                self.cfg.get_default_media_path(),
                home + 'SATORU_reddit' + sep)


if __name__ == '__main__':
    unittest.main()
