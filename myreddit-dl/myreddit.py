#!/usr/bin/env python3

"""
Author: Emanuel Ramirez Alsina (emanuel2718 @ Github)
Program: myreddit-dl
Description: Reddit upvoted & saved media downloader
"""
import sys
from reddit_client import RedditClient
from downloader import Downloader


def run():
    if len(sys.argv) > 1:
        Downloader().start()

    # GUI version of the app
    else:
        print('GUI version coming soon...')


if __name__ == '__main__':
    run()
