from myredditdl.defaults import Defaults


class Metadata:
    def __init__(self, debug=False):
        self.defaults = Defaults(debug)

    def show_metadata(self, filename: str):
        print(f'Metadata file: {self.defaults.metadata_file}')
        print(f'show_metadata request: {filename}')

    def show_link(self, filename: str):
        print(f'Metadata file: {self.defaults.metadata_file}')
        print(f'show_link request: {filename}')
