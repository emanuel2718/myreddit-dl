import json
from myredditdl.utils import setup_logger
from myredditdl.defaults import Defaults
from pprint import pprint


class Metadata:
    def __init__(self, debug=False):
        self.defaults = Defaults(debug)
        self.json_file = self.defaults.metadata_file
        self.log = setup_logger(__name__, debug)
        self.data = None

    def show_metadata(self, filename: str):
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if filename in data.keys():
                    print('\n')
                    pprint(data[filename])
                else:
                    self.log.info(f'Metadata for `{filename}` not found')
        except IOError:
            self.log.info('Database not found. Must download content first')

    def show_link(self, filename: str):
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if filename in data.keys():
                    print(f"\nLink: {data[filename]['Link']}")
                else:
                    self.log.info(f'Metadata for `{filename}` not found')
        except IOError:
            self.log.info('Database not found. Must download content first')
