#!/usr/bin/env python3

"""
Author: Emanuel Ramirez Alsina (emanuel2718 @ Github)
Program: myreddit-dl
Description: Reddit upvoted & saved media downloader
"""
import argparse
import console_args
import textwrap
import configparser
import logging
import utils
import sys
from gui import run_gui
from defaults import Defaults
from reddit_client import RedditClient
from downloader import Downloader


def run():
    # cli version of the app
    if len(sys.argv) > 1:
        # TODO: move me to file_handler.py
        #if cli_args['clean_debug']:
        #    Defaults().clean_debug()
        #    exit(0)

        reddit_client = RedditClient()
        reddit_client.build_reddit_instance()
        Downloader(reddit_client).start()

    # GUI version of the app
    else:
        print('GUI version coming soon...')


if __name__ == '__main__':
    run()
