<h1 align="center" style="font-size: 3rem;">
myreddit-dl
</h1>


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


