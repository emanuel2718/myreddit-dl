<div align="center">
<h1>My Reddit Downloader</h1>
<h4>Download upvoted and saved media from Reddit</h4>
</div>

&nbsp; 

**WARNING**: This is a work in progress. If you see this message, use at your own risk**

NOTE: When ready for production; this message will not be here and `myreddit-dl` will be found on PyPi

# Index

* [Requirements](#requirments)
* [Pre-Installation](#pre-installation)
* [Manual Installation](#manual-installation)
* [How to use](#how-to-use)
* [Advanced Configuration](#advanced-configuration)


# Requirements

- Python 3.6 or above
- requests
- praw

# Pre-Installation

[Create a developer application on reddit if needed](https://github.com/emanuel2718/myredditdl/blob/master/PRE_INSTALL.md)



# Manual Installation

&nbsp; 

### 1. Clone this repository
```sh
$ git clone https://github.com/emanuel2718/myredditdl
$ cd myredditdl
```

### 2. Install requirements
```sh
$ pip install -r requirements.txt
```

### 3. Install myredditdl
```sh
# you might need to install setuptools (pip install setuptools)
$ python3 setup.py install
```

### 4. Fill reddit developer app information
``` sh
$ myredditdl --add-client
```


# How to use
```sh
$ myredditdl [REQUIRED] [OPTIONS]
```

##### REQUIRED

    -U, --upvote            Download upvoted media
    -S, --saved             Download saved media


##### OPTIONS

&nbsp; 

###### Optional arguments:
    -h, --help                show this message and exit
    -v, --version             display the current version of myreddit-dl

    --sub [SUBREDDIT ...]     only download media that belongs to the given subreddit(s)
    --limit [LIMIT]           limit the amount of media to download (default: None)
    --max-depth [MAX_DEPTH]   maximum amount of posts to iterate through

    --no-video                don't download video files (.mp4, .gif, .gifv, etc.)
    --only-video              only download video files
    --no-nsfw                 disable NSFW content download
    
###### Confgiguration:
    --add-client              add a new Reddit account
    --change-client           change to another valid existing reddit client (account)
    --prefix OPT              set filename prefix (post author username and/or post subreddit name)
                              
                              Options:
                                  '--config-prefix username'           --> username_id.ext
                                  '--config-prefix username subreddit' --> username_subreddit_id.ext
                                  '--config-prefix subreddit username' --> subreddit_username_id.ext
                                  '--config-prefix subreddit'          --> subreddit_id.ext
                                  
                              Default: subreddit --> subreddit_id.ext
                              
    --path PATH               path to the folder were media will be downloaded to
    --get-config              prints the configuration file information to the terminal
    

###### Metadata:
    --no-metadata             don't save metadata for the downloaded media
    --get-metadata FILE       print all the reddit metadata of the given FILE
    --get-link FILE           print reddit link of given FILE
    --get-title FILE          print post title of given FILE
    --delete-database         delete the database of the current active reddit client user

# Configuration

Set the reddit client information to be able to use myredditdl
``` sh
$ myredditdl --add-client
```

Set the path to the destination folder for the downloaded media
``` sh
$ myredditdl --path ~/Path/to/destination
```

Set the filenames prefix scheme of the downloaded media
``` sh
# This will save all the files with the scheme: `postAuthorUsername_uniqueId.extension`
$ myredditdl --prefix username
```

``` sh
# This will save all the files with the scheme: `subredditName_postAuthorUsername_uniqueId.extension`
$ myredditdl --prefix subreddit username
```

``` sh
# This will save all the files with the scheme: `postAuthorName_subredditName_uniqueId.extension`
$ myredditdl --config-prefix username subreddit
```

Show the current configuration
``` sh
$ myredditdl --show-config
```

# Example usage:

Download all user upvoted media (limited to 1000 posts: Praw's API hard limit)
``` sh
$ myredditdl -U
```

Download all user saved media and don't save metadata of posts
``` sh
$ myredditdl -S --no-metadata
```

Download all user upvoted and saved media except NSFW posts
``` sh
$ myredditdl -U -S --no-nsfw
```

Download all the user upvoted posts from the r/MechanicalKeyboards subreddit

``` sh
$ myredditdl -U --sub MechanicalKeyboards
```

Download all the user upvoted posts from the r/MechanicalKeyboards and r/Battlestations subreddits

``` sh
# There's no limit to how many subreddits can be chained together
$ myredditdl -U --sub MechanicalKeyboards Battlestations
```

Download only 10 posts media and only download images (don't download videos)

``` sh
$ myredditdl -U --limit 10 --no-video
```

Get the post link of a downloaded media

``` sh
# This will print the reddit post link of that image
$ myredditdl --get-link random_image.png
```

Get the post title of a downloaded media

``` sh
# This will print the reddit post title of that video
$ myredditdl --get-title random_video.mp4
```

Get the metadata of downloaded media

``` sh
# This will print the metadata of the image
$ myredditdl --get-metadata random_image.jpg
```

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
- [x] Change `--save-metadata` to `--no-metadata` (Defaults to saving the metadata)
- [x] Why is __print_counters triggering twice sometimes?
- [x] write --debug information to debug.log file instead
- [x] Use `logging` module to improve logging
- [x] `--no-gallery` flag to skip gallery media
- [x] `--add-user` flag to add another profile.
- [x] `--change-user` flag to change to another profile if user has more than one account.
- [x] refactor downloader reddit post item into a separate Item class (item.py)
- [x] make a new module console_args.py and import it when needed. This is better than passing it everytime.
- [x] change `--nsfw` with `--no-nsfw`
- [ ] fix the `--help` configuration section. To long and cubersome to read
- [ ] change `None_` to `deleted_` for deleted accounts on file title
- [x] _, filename = os.path.split(full_path)
- [ ] entire refactorization of the project.
- [ ] think about refactoring argparser to be able to have it globally without instantiating or passing it
- [ ] In advanced configuration change configparser ['REDDIT'] to desired account (--change-user).
- [ ] Make test suite
- [ ] Fix path issues with ( ./ and / ), especially on Windows
- [ ] figure out why the stack trace log is repeating certain functions (get_base_path)...
- [ ] Make custom exceptions `exceptions.py`
- [ ] Optimize code!!
- [ ] upload to PyPy and add instruction here
- [ ] Add color to output (jupyter-notebook as an example)
- [ ] --clean-database flag that will remove all the links entries of files not longer present
- [ ] use item.link_flair_text to get tags. Some users might want items with certain tags only
- [ ] Handle case of repeated media (used --by-user and the --by-subreddit (duplicates))
- [ ] Use item.thumbnail picture for the GUI displays (maybe)

