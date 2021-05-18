DONT_RUN_THIS_FILE = ('This file is not intended to be run by itself. '
                      'See myreddit-dl -h for more information')


def print_debug(msg):
    print(f'[DEBUG] {msg}')


def print_error(msg):
    print(f'[ERROR] {msg}')


def print_failed(msg):
    print(f'[FAILED] {msg}')


def print_ok(msg):
    print(f'[OK] {msg}')


def print_warning(msg):
    print(f'[WARNING] {msg}')


if __name__ == '__main__':
    print_warning(DONT_RUN_THIS_FILE)
