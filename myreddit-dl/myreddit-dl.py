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

    parser.add_argument(
        '-U',
        '--upvote',
        action='store_true',
        help="Download upvoted media",
        required=False)

    parser.add_argument(
        '-S',
        '--saved',
        action='store_true',
        help="Download saved media",
        required=False)

    parser.add_argument(
        '-nsfw',
        action='store_true',
        help="Download NSFW content",
        required=False)

    # TODO: maybe add the option for more subreddits (i.e -sub sub_1 sub_2)
    parser.add_argument(
        '-sub',
        '--subreddit',
        type=str,
        nargs='*',
        help="Only download media that belongs to the given subreddit(s)",
        required=None)

    parser.add_argument(
        '-l',
        '--limit',
        type=int,
        help="Limit the amount of media to download (default: None)",
        required=None)

    parser.add_argument(
        '-v',
        '--version',
        help='displays the current version of myreddit-dl',
        action='store_true')

    parser.add_argument(
        '-debug',
        '--debug',
        action='store_true',
        help="Debug flag",
        required=False)

    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Print debugging information",
        required=False)

    parser.add_argument(
        '--save-links',
        action='store_true',
        help="Save post links in a file. Link database will be created if it doesn't exist.",
        required=False)

    parser.add_argument(
        '--no-video',
        action='store_true',
        help="Don't download video files (.mp4, .gif, .gifv, etc.)",
        required=False)

    parser.add_argument(
        '--get-link',
        type=str,
        help="Get the link to the post of the given media",
        required=False)

    parser.add_argument(
        '--max-depth',
        type=int,
        help="Maximum amount of posts to iterate through",
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
