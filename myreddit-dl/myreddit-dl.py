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
from gui import run_gui


def get_cli_args():
    # TODO: fix the usage once all the cli args are done
    parser = argparse.ArgumentParser(
        description='Reddit upvoted & saved media downloader',
        usage='myreddit-dl [-h] [-all] [-user] [-L LIMIT] [-s SUBREDDIT] [-p PATH]',
        formatter_class=argparse.RawTextHelpFormatter)


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
        '-t',
        '--title',
        action='store_true',
        help="Saved media with post link as filename",
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

    #parser.add_argument(
    #    '-p',
    #    '--path',
    #    help="Save on the given path",
    #    nargs='?',
    #    dest='path',
    #    const=None,
    #    metavar='PATH')

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
