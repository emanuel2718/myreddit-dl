import os
import logging
import unittest
from unittest import mock
from unittest.mock import patch
from unittest.mock import mock_open
from myredditdl.config_handler import ConfigHandler
from tests.mock_utils import get_new_client
from tests.mock_utils import get_dir_path
from tests.mock_utils import get_valid_options


class TestConfigHandler(unittest.TestCase):
    MOCK_FILE = get_dir_path()
    VALID_OPTIONS = get_valid_options()

    def setUp(self):
        self.cfg = ConfigHandler()
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_available_reddit_clients(self):
        sections = ['DEFAULTS', 'USERS', 'EMPTY_CLIENT', 'FIRST', 'SECOND']
        with patch.object(ConfigHandler, 'get_config_sections', return_value=sections):
            self.assertEqual(
                self.cfg.get_available_reddit_clients(), [
                    'FIRST', 'SECOND'])

    @mock.patch('builtins.open', new_callable=mock_open())
    @mock.patch('myredditdl.config_handler.ConfigHandler.get_config_path')
    @mock.patch('myredditdl.config_handler.ConfigHandler.get_client_active_section')
    def test_add_client(self, client, cfg_path, mock_open):
        client.return_value = 'EMPTY_CLIENT'
        cfg_path.return_value = self.MOCK_FILE
        self.assertFalse(self.cfg.add_client(get_new_client('EMPTY_CLIENT')))
        self.assertTrue(self.cfg.add_client(get_new_client('NEW_USER')))

    @mock.patch('builtins.open', new_callable=mock_open())
    @mock.patch('myredditdl.config_handler.ConfigHandler.get_config_path')
    @mock.patch('myredditdl.config_handler.ConfigHandler.get_client_active_section')
    def test_set_new_current_user(self, client, cfg_path, mock_open):
        client.return_value = 'EMPTY_CLIENT'
        cfg_path.return_value = self.MOCK_FILE
        self.assertFalse(self.cfg.set_new_current_user('EMPTY_CLIENT'))
        self.assertFalse(self.cfg.set_new_current_user('EMPTY_CLIENT'))
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
        home = os.path.expanduser('~/Pictures/')
        with patch.object(ConfigHandler, 'get_client_active_section', return_value='SATORU'):
            self.assertEqual(
                self.cfg.get_default_media_path(),
                home + 'SATORU_reddit' + os.sep)


if __name__ == '__main__':
    unittest.main()
