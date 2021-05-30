#!/usr/bin/env python3

"""
Author: Emanuel Ramirez Alsina (emanuel2718 @ Github)
Program: myreddit-dl
Description: Reddit upvoted & saved media downloader
"""
import argparse
import configparser
import sys
from gui import run_gui
from reddit_client import RedditClient
from downloader import Downloader


def get_cli_args():
    # TODO: fix the usage once all the cli args are done
    parser = argparse.ArgumentParser(
        description='Reddit user upvoted & saved media downloader',
        usage='myreddit-dl [-h] [-all] [-user] [-L LIMIT] [-s SUBREDDIT] [-p PATH]',
        formatter_class=argparse.RawTextHelpFormatter)

    required_group = parser.add_argument_group('Required Arguments')
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
        '--sub',
        type=str,
        nargs='*',
        help="only download media that belongs to the given subreddit(s)",
        required=None)

    parser.add_argument(
        '--limit',
        type=int,
        help="limit the amount of media to download (default: None)",
        required=None)

    parser.add_argument(
        '--max-depth',
        type=int,
        help="Maximum amount of posts to iterate through",
        required=False)

    parser.add_argument(
        '--no-video',
        action='store_true',
        help="Don't download video files (.mp4, .gif, .gifv, etc.)",
        required=False)

    parser.add_argument(
        '--only-video',
        action='store_true',
        help="Only download video files (.mp4, .gif, .gifv, etc.)",
        required=False)

    parser.add_argument(
        '-nsfw',
        '--nsfw',
        action='store_true',
        help="Enable NSFW content download",
        required=False)

    metadata_group.add_argument(
        '--save-metadata',
        action='store_true',
        help="Save post metadata in a file. Link, title, and number of upvotes of the post",
        required=False)

    metadata_group.add_argument(
        '--get-metadata',
        type=str,
        default=None,
        help="Print reddit metadata of a file if metadata for that file has been saved with --save-metadata",
        required=False)

    metadata_group.add_argument(
        '--get-link',
        type=str,
        help="Get the reddit post link of the given media",
        required=False)

    metadata_group.add_argument(
        '--get-title',
        type=str,
        help="Get the post title of the given media",
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
        run_gui()


if __name__ == '__main__':
    run()
