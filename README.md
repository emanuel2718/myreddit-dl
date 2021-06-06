<div align="center">
<h1>My Reddit Downloader</h1>
<h4>Download upvoted and saved media from Reddit</h4>
</div>

&nbsp; 

NOTE: This is a work in progress not all features are yet implemented. When this is ready for production this message will not be here and `myreddit-dl` will be found on PyPi

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

&nbsp; 

### 1. Clone this repository
```sh
$ git clone https://github.com/emanuel2718/myreddit-dl
$ cd myreddit-dl
```

### 2. Install requirements
```sh
$ pip install -r requirements.txt
```

### 3. Fill reddit developer app information in `myreddit-dl/config.ini`


# How to use
```sh
$ python3 myreddit-dl [REQUIRED] [OPTIONS]
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
    --nsfw                    enable NSFW content download (default: False)
    
###### Confgiguration:
    --config-save OPT         change how the filenames are saved (by username or subreddit)

###### Metadata:
    --save-metadata           enable this to save downloaded media metadata in a file
    --get-metadata FILE       print reddit metadata of given FILE
    --get-link FILE           print reddit link of given FILE
    --get-title FILE          print post title of given FILE

# Advanced Configuration

coming soon

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
- [x] Make flag to store in either: sub_user_id.ext or user_id.ext (eliminate sub folders?)
- [x] Fix bug caused by using getcwd() in entire codebase...
- [x] Handle case where path and username are empy in `config.ini`
- [x] Refactor `filename_save` to `filename_prefix`
- [x] Allow the user to `--config-save subreddit username` for subreddit_user_id.ext
- [x] Give the user the option to insert the credentials if no credentials are found.
- [x] If config.ini is empty run script to ask user for the information
- [x] Sanitize metadata titles (remove unicode characters)
- [x] Add flag --get-path that prints the current set path and --get-filesave
- [ ] Improve loggin messages (regular and --debug)
- [ ] In advanced configuration change configparser ['REDDIT'] to desired account (--change-user).
- [ ] Make custom exceptions `exceptions.py`
- [ ] --clean-database flag that will remove all the links entries of files not longer present
- [ ] use item.link_flair_text to get tags. Some users might want items with certain tags only
- [ ] Handle case of repeated media (used --by-user and the --by-subreddit (duplicates))
- [ ] Make test suite
- [ ] Add logging of adding to path on which we are saving media
- [ ] upload to PyPy and add instruction here
- [ ] Use item.thumbnail picture for the GUI displays (maybe)
- [ ] make a last_seen.txt file and include the item that was last downloaded

