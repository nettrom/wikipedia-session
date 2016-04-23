# Copyright (C) 2016 Ben Lewis, and Morten Wang
# Licensed under the MIT license, see ../LICENSE

# Question: When was the first edit to the panama papers wikipedia article?
# Do it with loops this time

import requests

ENDPOINT = 'https://en.wikipedia.org/w/api.php'

parameters = { 'action' : 'query',
               'prop' : 'revisions',
               'titles' : "Panama_Papers",
               'format' : 'json',
               'rvlimit' : 1,
               'rvdir' : 'newer',
               'continue' : '' }


# get the first edit for a list of pages
page_titles = ['Panama_Papers','Douglas_Adams','Benjamin_Mako_Hill','Python_(programming_language)']

for page_title in page_titles:
    parameters['titles'] = page_title
    wp_call = requests.get(ENDPOINT, params=parameters)

    response = wp_call.json()

    query = response['query']

    pages = query['pages']

    # we can can also iterate through the dictionary
    for page_id in pages:
        page = pages[page_id]
        revisions = page['revisions']

        for revision in revisions:

            revid = revision['revid']
            revuser = revision['user']
            revdate = revision['timestamp']
            title = page['title']

            print('First edit to ' + title + ' was revision ID ' + str(revid) + ' by ' + revuser + ' on ' + revdate)
