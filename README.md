<div align="center">
<h1>My Reddit Downloader</h1>
<h4>Download upvoted and saved media from Reddit</h4>
</div>



# Index

* [Requirements](#requirments)
* [Pre-Installation](#pre-installation)
* [Installation](#installation)
* [How to use](#how-to-use)
* [Advanced Configuration](#advanced-configuration)


# Requirements

- Python 3.6 or above
- requests
- praw

# Pre-Installation

[Create a developer application on reddit if needed](https://github.com/emanuel2718/myreddit-dl/blob/master/PRE_INSTALL.md)



# Installation

- [PyPi](#pypi)
- [Manual Installation](#manual-installion)

### PyPi

0. Install using pip

    ```console
    pip install myreddit-dl
    ```

### Manual Installation

1. Clone this repository into desired location

    ```console
    git clone https://github.com/emanuel2718/myreddit-dl
    ```

2. Install `setuptools` from pip if needed

    ```console
    pip install setuptools
    ```

3. Cd into `myreddit-dl` and install
    ```console
    cd myreddit-dl
    sudo python setup.py install
    ```
    
# How to use

```console
myreddit-dl [REQUIRED] [OPTIONS]
```

##### REQUIRED

    -U, --upvote            Download upvoted media
    -S, --saved             Download saved media


##### OPTIONS

&nbsp; 

###### Optional arguments:
    -h, --help                show this message and exit
    -v, --version             display the current version of myreddit-dl
    -verbose, --verbose       print extra information while downloading

    --sub [SUBREDDIT ...]     only download media that belongs to the given subreddit(s)
    --limit [LIMIT]           limit the amount of media to download (default: None)
    --max-depth [MAX_DEPTH]   maximum amount of posts to iterate through

    --no-video                don't download video files (.mp4, .gif, .gifv, etc.)
    --only-video              only download video files
    --nsfw, --nsfw             enable NSFW content download (default: False)

###### Metadata:
    --save-metadata           enable this to save downloaded media metadata in a file
    --get-metadata FILE       print reddit metadata of given FILE
    --get-link FILE           print reddit link of given FILE
    --get-title FILE          print post title of given FILE

# Advanced Configuration

# TODOLIST
- [x] --max-depth argument for max number of posts to search
- [x] Make a link file (.user_links.txt)
- [x] Make a --no-video flag
- [x] use permalink to save with post title (append reddit.com)
- [x] refactor absolute_path + url from gallery_data posts...
- [x] `--only-videos` flag?
- [x] refactor entirely link saving to metadata saving for --get-metadata
- [x] `--get-metadata` --> User, title, link, user karma, sub, amount of upvotes...
- [x] `--get-title` flag in which the title of the given image is returned.
- [ ] If config.ini is empty run script to ask user for the information
- [ ] Clean titles (remove unicodes like \u00f1)
- [ ] use os.path.expanduser('~') for home dir
- [ ] Add logging of adding to path on which we are saving media
- [ ] improve logging messages
- [ ] Make custom exceptions `exceptions.py`
- [ ] allow the user to enter custom paths `-p, --path` to download media to.
- [ ] fix argparser description
- [ ] --clean-database flag that will remove all the links entries of files not longer present
- [ ] Use item.thumbnail picture for the GUI displays (maybe)
- [ ] make a last_seen.txt file and include the item that was last downloaded

