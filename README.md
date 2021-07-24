[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<div align="center">
<h1>My Reddit Downloader</h1>
<h4>Download upvoted and saved media from Reddit</h4>
</div>

&nbsp; 


# Index

* [Requirements](#requirments)
* [Pre-Installation](#pre-installation)
* [Installation](#installation)
* [Manual Installation](#manual-installation)
* [How to use](#how-to-use)
* [Advanced Configuration](#advanced-configuration)


# Requirements

- Python 3.6 or above
- requests
- praw

# Pre-Installation

[Create a developer application on reddit if needed](https://github.com/emanuel2718/myredditdl/blob/master/PRE_INSTALL.md)

# Installation

``` sh
pip install myredditdl
```

&nbsp; 

# Manual Installation


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
