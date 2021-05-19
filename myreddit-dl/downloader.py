import cli
from file_handler import get_filename

class Downloader:
    def __init__(self, client):
        self.client = client
        self.args = client.get_args()
        self.username = client.get_user()
        self.upvoted = client.get_user_upvotes()
        self.saved = client.get_user_saves()
        self.subreddit_list = self.args['subreddit']
        self.by_user = self.args['user']
        self.limit = self.args['limit']
        self.download_counter = 0
        self.run()

    def download_limit_reached(self):
        if self.limit is None or self.download_counter < self.limit:
            return False
        return True

    def download(self, filename, item):
        pass

    def run(self):
        for item in self.upvoted:
            if not self.download_limit_reached():
                # TODO: think about making a FileHandler class instead
                filename = get_filename(self.args, self.username, item)
                print(filename)
                self.download(filename, item)
            else:
                break





if __name__ == '__main__':
    cli.print_warning(cli.DONT_RUN_THIS_FILE)
