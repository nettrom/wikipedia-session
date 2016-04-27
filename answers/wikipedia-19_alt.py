# Copyright (C) 2016 Ben Lewis, and Morten Wang
# Licensed under the MIT license, see ../LICENSE

import requests
from urllib.parse import quote

ENDPOINT = 'https://en.wikipedia.org/w/api.php'

# Who is the most popular person mentioned in the Panama Papers article?
# We'll define "most popular" as the living person with the most views
# since the papers were released.

# This query uses the links as a generator to get the categories
# for the linked pages, and restricts the categories to only look for
# 'Category:Living people'. That allows us to iterate over the pages
# and find the living people in the first step.
parameters = { 'action' : 'query',
               'prop' : 'categories',
               'generator': 'links',
               'gpllimit': 500,
               'titles' : 'Panama Papers',
               'format' : 'json',
               'cllimit' : 500,
               'clcategories' : 'Category:Living people',
               'redirects' : 'true',
               'continue' : '' }

# There's also a list of people mentioned in the papers:
# parameters['titles'] = 'List of people named in the Panama Papers'

living_people = [] # list of living people
people_popularity = {} # keys are people, values are number of views

# 1: Find all living people mentioned in the article
num_iterations = 0
done = False
while not done:
    wp_call = requests.get(ENDPOINT, params=parameters)
    response = wp_call.json()

    num_iterations += 1
    print('Current iteration: ' + str(num_iterations))

    pages = response['query']['pages']
    for page in pages:
        # Note: because we set 'clcategories' we only need to test for
        # the key, it will be missing if the article isn't in that category.
        if 'categories' in pages[page]:
            living_people.append(pages[page]['title'])

    # Note: because we're using a generator, the key is 'gplcontinue'
    if 'continue' in response:
        parameters['continue'] = response['continue']['continue']
        parameters['gplcontinue'] = response['continue']['gplcontinue']
    else:
        done = True

print('There are ' + str(len(living_people)) + ' living people linked')

# 2: get the popularity of each of these
ENDPOINT = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/'

wp_code = 'en.wikipedia'
access = 'all-access'
agents = 'all-agents'
period = 'daily'
start_date = '20160403'
end_date = '20160421'

for person in living_people:
    print('Getting views for ' + person)
    wp_call = requests.get(ENDPOINT + wp_code + '/' + access + '/' + agents + '/' + quote(person, safe='') + '/' + period + '/' + start_date + '/' + end_date)
    response = wp_call.json()

    people_popularity[person] = 0 # initalise to 0
    if 'items' in response: # did we get any views?
        for item in response['items']:
            people_popularity[person] += item['views']

# 3: Sort by popularity and write out
from operator import itemgetter
sorted_people = sorted(people_popularity.items(),
                       key=itemgetter(1),
                       reverse=True)
print('Top 10:')
for (person, views) in sorted_people[:10]:
    print(person + ' had ' + str(views) + ' views')
