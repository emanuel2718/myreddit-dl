#!/usr/bin/env python3

"""
Author: Emanuel Ramirez Alsina (emanuel2718 @ Github)
Program: myredditdl
Description: Reddit upvoted & saved media downloader
"""
import sys
import myredditdl.console_args as console_args
from myredditdl.downloader import Downloader


def run():
    if len(sys.argv) > 1:
        console_args.check_requests()
        Downloader().start()

    # GUI version of the app
    else:
        print('GUI version coming soon...')


if __name__ == '__main__':
    run()
