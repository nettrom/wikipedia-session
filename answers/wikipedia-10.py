# Copyright (C) 2016 Ben Lewis, and Morten Wang
# Licensed under the MIT license, see ../LICENSE

import requests

ENDPOINT = 'https://en.wikipedia.org/w/api.php'

parameters = { 'action' : 'query',
               'prop' : 'revisions',
               'titles' : 'Panama Papers',
               'format' : 'json',
               'rvdir' : 'newer',
               'rvstart': '2016-04-03T17:59:05Z',
               'rvend' : '2016-04-10T17:59:05Z',
               'rvlimit' : 500,
               'continue' : '' }

num_revisions = 0

done = False
while not done:
    wp_call = requests.get(ENDPOINT, params=parameters)
    response = wp_call.json()

    for page in response['query']['pages']:
        for revision in response['query']['pages'][page]['revisions']:
            num_revisions = num_revisions + 1

    print('Done one query, num revisions is now ' + str(num_revisions))

    if 'continue' in response:
        parameters['continue'] = response['continue']['continue']
        parameters['rvcontinue'] = response['continue']['rvcontinue']
    else:
        done = True

print(parameters['titles'] + ' had ' + str(num_revisions) + ' revisions in the first 24 hours')
