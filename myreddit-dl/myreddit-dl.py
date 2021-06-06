#!/usr/bin/env python3

"""
Author: Emanuel Ramirez Alsina (emanuel2718 @ Github)
Program: myreddit-dl
Description: Reddit upvoted & saved media downloader
"""
import argparse
import textwrap
import configparser
import sys
from gui import run_gui
from reddit_client import RedditClient
from downloader import Downloader


def get_cli_args():
    parser = argparse.ArgumentParser(
        description='Reddit upvoted & saved media downloader',
        usage='myreddit-dl [-h] [REQUIRED] [OPTIONS]',
        formatter_class=argparse.RawTextHelpFormatter)

    required_group = parser.add_argument_group(
        'Required Arguments (only required to download)')

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
        '--client-config',
        action='store_true',
        help="change the reddit app client information (id, secret, username, password)",
        required=False)

    config_group.add_argument(
        '--get-config',
        action='store_true',
        help="prints the configuration file information to the terminal",
        required=False)

    config_group.add_argument(
        '--get-config-show',
        action='store_true',
        help="prints the configuration file information to the terminal and show password",
        required=False)

    config_group.add_argument(
        '--config-prefix',
        type=str,
        nargs='*',
        default=None,
        help=textwrap.dedent('''\
        set filename prefix (post author username and/or post subreddit name)

        Options:

            '--config-prefix username'           ---> username_id.extension
            '--config-prefix username subreddit' ---> username_subreddit_id.extension
            '--config-prefix subreddit username' ---> subreddit_username_id.exension
            '--config-prefix subreddit'          ---> subreddit_id.exension

        Default: subreddit ---> subreddit_id.extension

        '''),
        metavar='OPT',
        required=False)

    config_group.add_argument(
        '--config-path',
        type=str,
        default=None,
        help=textwrap.dedent('''\
        path to the folder were media will be downloaded to

        Examples:

        To download the media to the folder ~/Pictures/reddit_media:
            --config-path $HOME/Pictures/reddit_media
                                or
            --config-path ~/Pictures/reddit_media

        To download the media to the current working directory:
            --config-path ./

        To download the media to a folder in the current working directory
            --config-path ./random_folder_destination

        Default Path: $HOME/Pictures/User_myreddit/
        '''),
        metavar='PATH',
        required=False)

    parser.add_argument(
        '-debug',
        '--debug',
        action='store_true',
        help="Debug flag",
        required=False)

    parser.add_argument(
        '-v',
        '--version',
        help='displays the current version of myreddit-dl',
        action='store_true')

    parser.add_argument(
        '-verbose',
        '--verbose',
        action='store_true',
        help="print debugging information",
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
        '--nsfw',
        action='store_true',
        help="enable NSFW content download",
        required=False)

    parser.add_argument(
        '--sub',
        type=str,
        nargs='*',
        help="only download media that belongs to the given subreddit(s)",
        metavar='SUBREDDIT',
        required=None)

    metadata_group.add_argument(
        '--save-metadata',
        action='store_true',
        help="enable this to save the metadata of downloaded media in a file",
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

    return vars(parser.parse_args())


def run():

    # cli version of the app
    if len(sys.argv) > 1:
        cli_args = get_cli_args()
        reddit_client = RedditClient(cli_args)
        downloader = Downloader(reddit_client)

    # GUI version of the app
    else:
        print('GUI version coming soon...')
        # run_gui()


if __name__ == '__main__':
    run()
