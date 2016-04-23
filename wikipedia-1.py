# Copyright (C) 2016 Ben Lewis, and Morten Wang
# Licensed under the MIT license, see ../LICENSE

# Question: When was the first edit to the panama papers wikipedia article?

import requests

ENDPOINT = 'https://en.wikipedia.org/w/api.php'

page_title = 'Panama_Papers'

parameters = { 'action' : 'query',
               'prop' : 'revisions',
               'titles' : page_title,
               'format' : 'json',
               'rvlimit' : 1,
               'rvdir' : 'newer',
               'continue' : '' }

# explain what the parameters mean:
'''
This is documented in the API sandbox. Don't worry about remembering it. 
Use the reference. 

'action' : 'query'  -- don't worry about this.
'prop' : 'revisions' -- this means we are asking for information about edits.
'titles' : 'Panama_Papers' -- this means we want information about the page called "Panama Papers". 
'format' : 'json' -- get the response in json, we won't change this. 
'rvlimit' : 1 -- get one revision
'rvdir' : 'newer' -- this means get the oldest revision first. use 'older' to get the newest edit first.
'continue' : '' -- we will cover this later!
'''

wp_call = requests.get(ENDPOINT, params=parameters)

response = wp_call.json()

# look at the json response
# print(response)

# The query dictionary holds the response to our "query"
query = response['query']

# The wikipedia api allows to you query about multiple pages
# We can ignore this, since we only queried about one page
pages = query['pages']

# get the page we asked for.
# this is a little complicated because pages is a dictionary
page_keys = list(pages.keys())
page_key = page_keys[0]
page = pages[page_key]

# the page dictionary has a 'revisions' item. this has the data revisions that we seek
revisions = page['revisions']

# we only asked for one revision
revision = revisions[0]

revid = revision['revid']
revuser = revision['user']
revdate = revision['timestamp']
title = page['title']

print('First edit to ' + title + ' was revision ID ' + str(revid) + ' by ' + revuser + ' on ' + revdate)
