# Copyright (C) 2016 Ben Lewis, and Morten Wang
# Licensed under the MIT license, see ../LICENSE

import requests

ENDPOINT = 'https://en.wikipedia.org/w/api.php'

parameters = { 'action' : 'query',
               'prop' : 'revisions',
               'titles' : 'Panama Papers',
               'format' : 'json',
               'rvlimit' : 1,
               'rvdir' : 'newer',
               'continue' : '' }

wp_call = requests.get(ENDPOINT, params=parameters)

response = wp_call.json()

for page in response['query']['pages']:
    for revision in response['query']['pages'][page]['revisions']:
        print('First edit to ' + parameters['titles'] + ' was revision ID ' + str(revision['revid']) + ' by ' + revision['user'] + ' on ' + revision['timestamp'])
