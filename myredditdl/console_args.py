import argparse
import textwrap
import myredditdl.utils as utils
from myredditdl.terminal import Terminal
from myredditdl.config_handler import ConfigHandler


def __mapped_config_requests():
    terminal = Terminal()
    return {'add_client': terminal.client_setup,
            'change_client': terminal.change_client,
            'show_config': ConfigHandler().__print__,
            'path': terminal.change_path,
            'prefix': terminal.change_prefix}


def check_config_requests():
    args = get_console_args()
    for request, func_call in __mapped_config_requests().items():
        if args[request]:
            func_call(args[request])
            exit(0)


def get_console_args():
    parser = argparse.ArgumentParser(
        description='Reddit upvoted & saved media downloader',
        usage='myredditdl [-h] [REQUIRED] [OPTIONS]',
        formatter_class=argparse.RawTextHelpFormatter)

    required_group = parser.add_argument_group(
        'Required Arguments')

    config_group = parser.add_argument_group('Configuration')
    metadata_group = parser.add_argument_group('Metadata')

    required_group.add_argument(
        '-U',
        '--upvote',
        action='store_true',
        help="Download upvoted media",
        required=False)

    required_group.add_argument(
        '-S',
        '--saved',
        action='store_true',
        help="Download saved media",
        required=False)

    config_group.add_argument(
        '--add-client',
        action='store_true',
        help=textwrap.dedent('''\
        add new reddit account

        '''),
        required=False)

    config_group.add_argument(
        '--change-client',
        action='store_true',
        help=textwrap.dedent('''\
        change to another valid existing reddit client (account)

        '''),
        required=False)

    config_group.add_argument(
        '--prefix',
        type=str,
        nargs='*',
        default=None,
        help=textwrap.dedent('''\
        set filename prefix (post author username and/or post subreddit name)

        Options:

            --prefix username           ---> username_id.extension
            --prefix username subreddit ---> username_subreddit_id.extension
            --prefix subreddit username ---> subreddit_username_id.exension
            --prefix subreddit          ---> subreddit_id.exension

        Default: subreddit_username ---> subreddit_username_id.extension

        '''),
        metavar='OPT',
        required=False)

    config_group.add_argument(
        '--path',
        type=str,
        default=None,
        help='set the path to the folder were media will be downloaded to',
        metavar='PATH',
        required=False)

    config_group.add_argument(
        '--show-config',
        action='store_true',
        help="print current configuration to the terminal",
        required=False)

    parser.add_argument(
        '-v',
        '--version',
        help='displays the current version of myredditdl',
        action='store_true')

    parser.add_argument(
        '-debug',
        '--debug',
        action='store_true',
        help='debug flag',
        required=False)

    parser.add_argument(
        '--limit',
        type=int,
        help="limit the amount of media to download (default: None)",
        required=None)

    parser.add_argument(
        '--max-depth',
        type=int,
        help="maximum amount of posts to iterate through",
        metavar='DEPTH',
        required=False)

    parser.add_argument(
        '--no-gallery',
        action='store_true',
        help="don't download galleries (posts with more than one image/video)",
        required=False)

    parser.add_argument(
        '--no-video',
        action='store_true',
        help="don't download video files",
        required=False)

    parser.add_argument(
        '--only-video',
        action='store_true',
        help="only download video files",
        required=False)

    parser.add_argument(
        '--no-nsfw',
        action='store_true',
        help="disable NSFW content download",
        required=False)

    parser.add_argument(
        '--sub',
        type=str,
        nargs='*',
        help="only download media that belongs to the given subreddit(s)",
        metavar='SUBREDDIT',
        required=None)

    parser.add_argument(
        '--clean-debug',
        action='store_true',
        help="remove all debug files",
        required=False)

    metadata_group.add_argument(
        '--no-metadata',
        action='store_true',
        help="don't save metadata for the downloaded media",
        required=False)

    metadata_group.add_argument(
        '--get-metadata',
        type=str,
        default=None,
        help="print reddit metadata of given FILE",
        metavar='FILE',
        required=False)

    metadata_group.add_argument(
        '--get-link',
        type=str,
        help="print reddit link of given FILE",
        metavar='FILE',
        required=False)

    metadata_group.add_argument(
        '--get-title',
        type=str,
        help="print post title of given FILE",
        metavar='FILE',
        required=False)

    metadata_group.add_argument(
        '--delete-database',
        action='store_true',
        help="delete the database of the current active reddit client user",
        required=False)

    return vars(parser.parse_args())


if __name__ == '__main__':
    utils.DONT_RUN_THIS_FILE
