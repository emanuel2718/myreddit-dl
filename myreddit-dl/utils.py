# Domains and usefuls urls
REDDIT_GALLERY_URL = 'https://www.reddit.com/gallery/'
NSFW_DOMAINS = {'redgifs.com', 'erome.com'}
SFW_DOMAINS = {'v.redd.it', 'i.redd.it', 'i.imgur.com',
               'gfycat.com', 'streamable.com', 'reddit.com', 'imgur.com'}

SUPPORTED_MEDIA_FORMATS = ('.jpg', '.png', '.jpeg', '.gif', '.gifv', '.mp4')
EXTENSION_STRING = '.jpg.png.jpeg.gif.gifv.mp4'

# Usefuls messages
DONT_RUN_THIS_FILE = ('This file is not intended to be run by itself. '
                      'See myreddit-dl -h for more information')

USER_NOT_FOUND = 'User not found. Make sure the `config.ini` file is correct.\n'


# Helper printing functions
def print_debug(msg: str) -> None:
    print(f'[DEBUG] {msg}')


def print_done(msg: str) -> None:
    print(f'[DONE] {msg}')


def print_error(msg: str) -> None:
    print(f'[ERROR] {msg}')


def print_failed(msg: str) -> None:
    print(f'[FAILED] {msg}')


def print_file_added(filename: str) -> None:
    print(f'[ADDED] {filename}')


def print_already_exists(filename: str) -> None:
    print(f'[ALREADY EXISTS] {filename}')


def print_file_removed(filename: str) -> None:
    print(f'[DELETE] {filename}')


def print_info(msg: str) -> None:
    print(f'[INFO] {msg}')


def print_editing(msg: str) -> None:
    print(f'[EDITING] {msg}')


def print_ok(msg: str) -> None:
    print(f'[OK] {msg}')


def print_warning(msg: str) -> None:
    print(f'[WARNING] {msg}')


if __name__ == '__main__':
    print_warning(DONT_RUN_THIS_FILE)
