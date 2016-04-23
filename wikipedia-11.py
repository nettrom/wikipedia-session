# Copyright (C) 2016 Ben Lewis, and Morten Wang
# Licensed under the MIT license, see ../LICENSE

# Who made the most edits to the article?

import requests

ENDPOINT = 'https://en.wikipedia.org/w/api.php'

parameters = { 'action' : 'query',
               'prop' : 'revisions',
               'titles' : 'Panama_Papers',
               'format' : 'json',
               'rvdir' : 'newer',
               'rvstart': '2016-04-03T17:59:05Z',
               'rvend' : '2016-04-23T17:59:05Z',
               'rvlimit' : 500,
               'continue' : '' }

num_revisions = 0

done = False
user_edits = {}
while not done:
    wp_call = requests.get(ENDPOINT, params=parameters)
    response = wp_call.json()

    pages = response['query']['pages']
    
    for page_id in pages:
        page = pages[page_id]
        revisions = page['revisions']
        for revision in revisions:
            revuser = revision['user']
            num_revisions = num_revisions + 1
            if revuser in user_edits:
                user_edits[revuser] = user_edits[revuser] + 1
            else:
                user_edits[revuser] = 1

    print('Done one query, num revisions is now ' + str(num_revisions))

    if 'continue' in response:
        parameters['continue'] = response['continue']['continue']
        parameters['rvcontinue'] = response['continue']['rvcontinue']
    else:
        done = True

top_editors = []
max_edits = 0
for user in user_edits:
    num_edits = user_edits[user]
    if num_edits > max_edits:
        max_edits = num_edits
        top_editors = [user]
    elif num_edits == max_edits:
        top_editors.append(user)
    else:
        pass

print(str(top_editors) + ' had the most edits with ' + str(max_edits))
