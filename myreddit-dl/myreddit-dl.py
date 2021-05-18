#!/usr/bin/env python3

"""
Author: Emanuel Ramirez Alsina (emanuel2718 @ Github)
Program: myreddit-dl
Description: Reddit upvoted & saved media downloader
"""
import argparse
import configparser
import sys
from cli import run_cli
from gui.gui_launcher import run_gui


def get_cli_args():
    parser = argparse.ArgumentParser(
        description='Reddit upvoted & saved media downloader',
        usage='myreddit-dl [-h] [-all] [-user] [-L LIMIT] [-s SUBREDDIT] [-p PATH]',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-debug',
        '--debug',
        action='store_true',
        help="Debug flag",
        required=False)

    parser.add_argument(
        '-all',
        action='store_true',
        help="Download every user upvoted posts",
        required=False)

    parser.add_argument(
        '-user',
        action='store_true',
        help="Save with post author name in front of file name",
        required=False)

    parser.add_argument(
        '-l',
        '--limit',
        type=int,
        help="Limit of post to download (default: None)",
        required=None)

    parser.add_argument(
        '-s',
        '--subreddit',
        type=str,
        help="Only save post that belong to the given subreddit",
        required=None)

    parser.add_argument(
        '-p',
        '--path',
        help="Save on the given path",
        nargs='?',
        dest='path',
        const=None,
        metavar='PATH')

    return vars(parser.parse_args())


def main():

    # cli version of the app
    if len(sys.argv) > 1:
        cli_args = get_cli_args()
        run_cli(cli_args)

    # GUI version of the app
    else:
        run_gui()


if __name__ == '__main__':
    main()
