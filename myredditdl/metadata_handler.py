import json
from myredditdl.utils import setup_logger
from myredditdl.defaults import Defaults
from pprint import pprint


class Metadata:
    def __init__(self, debug=False):
        self.defaults = Defaults(debug)
        self.json_file = self.defaults.metadata_file
        self.log = setup_logger(__name__, debug)
        self._metadata_map = {}

    def add_to_map(self, filename: str, metadata: dict) -> None:
        ''' Adds a dictionary entry {filename: {metadata}} to the
            metadata map.

        @params:
            - filename: the filename of the entry
            - metadata: reddit post metadata associated to the given filename
        '''
        self._metadata_map[filename] = metadata

    def get_map(self) -> dict:
        ''' Returns the metadata map composed of one or more
            {filename: reddit metadata}

        @return: dictionary of the following format
                 {filename: {metadata}, filename: {metadata}, ...}

        Note: filenames are the keys of the map
        '''
        return self._metadata_map

    def show_metadata(self, filename: str):
        ''' Prints to the console the Reddit post metadata associated
            with the given @filename if it is found.
        '''
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
        ''' Prints to the console the Reddit post URL link of the given
            media filename.
        '''
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if filename in data.keys():
                    print(f"\nLink: {data[filename]['Link']}")
                else:
                    self.log.info(f'Metadata for `{filename}` not found')
        except IOError:
            self.log.info('Database not found. Must download content first')
