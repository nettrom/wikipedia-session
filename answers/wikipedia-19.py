# Copyright (C) 2016 Ben Lewis, and Morten Wang
# Licensed under the MIT license, see ../LICENSE

import requests
from urllib.parse import quote

<<<<<<< HEAD
# Notes:
# 1: documentation https://wikimedia.org/api/rest_v1/?doc
# 2: there is no view data for 20160403, bug?

=======
ENDPOINT = 'https://en.wikipedia.org/w/api.php'

# Or use:
# 'titles' : 'List of people named in the Panama Papers',
parameters = { 'action' : 'query',
               'prop' : 'links',
               'titles' : 'Panama Papers',
               'format' : 'json',
               'pllimit' : 500,
               'redirects' : 'true',
               'continue' : '' }

# Who is the most popular person mentioned in the Panama Papers article?
# We'll define "most popular" as the living person with the most views
# since the papers were released.

linked_articles = [] # all articles linked from Panama Papers
living_people = [] # articles that are in "Category:Living people"
people_popularity = {} # keys are people, values are number of views

# 1: Find all living people mentioned in the article

# 1.1: Find all links from Panama Papers to other articles
num_iterations = 0
done = False
while not done:
    wp_call = requests.get(ENDPOINT, params=parameters)
    response = wp_call.json()

    num_iterations += 1
    print('Current iteration: ' + str(num_iterations))
    
    for page in response['query']['pages']:
        links = response['query']['pages'][page]['links']
        for link in links:
            if link['ns'] == 0: # is this an article?
                linked_articles.append(link['title'])
    if 'continue' in response:
        parameters['continue'] = response['continue']['continue']
        parameters['plcontinue'] = response['continue']['plcontinue']
    else:
        done = True

print('There are ' + str(len(linked_articles)) + ' articles linked from Panama Papers')
        
# 1.2: For each link, get the article's categories and check if "Living people"
#      is one of them.
# Note: Step 1.1 & 1.2 can be done in a single query, but that is outside
#       the scope of this lesson. If you're curious about how it's done,
#       see wikipedia-19_alt.py

parameters = { 'action' : 'query',
               'prop' : 'categories',
               'titles' : None, # we'll fill that in later
               'format' : 'json',
               'cllimit' : 500,
               'redirects' : 'true', # automatically resolve redirects, please
               'continue' : '' }

for article in linked_articles:
    print('Checking if ' + article + ' is a living person')
    parameters['titles'] = article

    num_iterations = 0
    done = False
    while not done:
        wp_call = requests.get(ENDPOINT, params=parameters)
        response = wp_call.json()

        num_iterations += 1
        print('Current iteration: ' + str(num_iterations))
    
        for page in response['query']['pages']:
            # We have to test for 'categories' as otherwise articles that don't
            # exist will crash the program.
            if 'categories' in response['query']['pages'][page]:
                categories = response['query']['pages'][page]['categories']
                for category in categories:
                    if category['title'] == 'Category:Living people':
                        living_people.append(article)
                        done = True

        if 'continue' in response:
            parameters['continue'] = response['continue']['continue']
            parameters['plcontinue'] = response['continue']['plcontinue']
        else:
            done = True

print('There are ' + str(len(living_people)) + ' living people linked from Panama Papers')
            
# 2: get the popularity of each of these
>>>>>>> 6fe97ad06d785f26c6434acb530c14ef98637c6c
ENDPOINT = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/'

wp_code = 'en.wikipedia'
access = 'all-access'
agents = 'all-agents'
<<<<<<< HEAD
page_title = 'Panama Papers'
period = 'daily'
start_date = '20160404'
end_date = '20160423'

wp_call = requests.get(ENDPOINT + wp_code + '/' + access + '/' + agents + '/' + quote(page_title, safe='') + '/' + period + '/' + start_date + '/' + end_date)
response = wp_call.json()

max_days = []
max_views = 0
for item in response['items']:
    views = item['views']
    day = item['timestamp']
    if views > max_views:
        max_views = views
        max_days = [day]
    elif views == max_views:
        max_days.append(day)
    else:
        pass

print(page_title + ' had the most views on ' + str(max_days))
print('with ' + str(max_views) + ' views')
=======
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

# 3: sort by popularity and write out
max_views = 0
max_people = []
for person, views in people_popularity.items():
    if views > max_views:
        max_views = views
        max_people = [person]
    elif views == max_views:
        max_people.append(person)

# Now, print out
print('The most popular people listed in the Panama Papers article are ' + str(max_people) + ' with ' + str(max_views) + ' views')

# Bonus: Using Python's sort to get the top ten
print('Top 10:')
from operator import itemgetter
sorted_people = sorted(people_popularity.items(),
                       key=itemgetter(1),
                       reverse=True)
for (person, views) in sorted_people[:10]:
    print(person + ' had ' + str(views) + ' views')
>>>>>>> 6fe97ad06d785f26c6434acb530c14ef98637c6c
