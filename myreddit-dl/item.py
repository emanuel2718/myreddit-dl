from datetime import datetime

# TODO: use this
# from collections import namedtuple
#
# Item = namedtuple('Item', 'id subreddit title user link upvotes nsfw')
# curr = Item('7dyu5', 'r/MechanicalKeyboards', 'This is a title',
#             'random_user', 'https://reddit.com/r/mecha..', '12452', True)
# print(curr)
#
# curr._fields
#  To make a dictionary. Damn!!!
# curr._make
# curr._asdict(u)

# It can be used as
# curr.id
# curr[0]

class Item:
    def __init__(self, item):
        self._item = item

    def __len__(self):
        return len(self._item)

    def __getitem__(self):
        return self._item

    def __repr__(self):
        # this should be unambigous and must match the object representation
        return 'Item(%r, %r, %r, %r %r)' % (self.item_id,
                                            self.title,
                                            self.link,
                                            self.subreddit_prefixed,
                                            self.author)


    def __str__(self):
        # This is called by the print() function and should return a string suitable for
        # display to end-users
        fmt = '{:6} = {}\n{:6} = {}\n{:6} = {}\n{:6} = {}\n{:6} = {}'
        return fmt.format('Id', self.item_id,
                          'Title', self.title,
                          'Link', self.link,
                          'Sub', self.subreddit_prefixed,
                          'Author', self.author)

    @property
    def title(self) -> str:
        return str(self._item.title)

    @property
    def item_id(self) -> str:
        return str(self._item.id)

    @property
    def link(self) -> str:
        return 'https://reddit.com' + str(self._item.permalink)

    @property
    def subreddit_name(self) -> str:
        return str(self._item.subreddit)

    @property
    def subreddit_prefixed(self) -> str:
        ''' Returns the item subreddit in the format r/Subreddit'''
        return str(self._item.subreddit_name_prefixed)

    @property
    def upvotes_amount(self) -> str:
        return str(self._item.ups)

    @property
    def author(self) -> str:
        return str(self._item.author)

    def is_nsfw(self) -> bool:
        return self._item.over_18

    def get_creation_date(self) -> str:
        time_utc = self._item.created_utc
        return str(datetime.fromtimestamp(time_utc).strftime('%m/%d/%Y'))
