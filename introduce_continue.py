import requests

ENDPOINT = 'https://en.wikipedia.org/w/api.php'

parameters = { 'action' : 'query',
               'prop' : 'revisions',
               'titles' : 'Panama_Papers',
               'format' : 'json',
               'rvdir' : 'newer',
               'rvstart': '2016-04-03T17:59:05Z',
               'rvend' : '2016-04-04T17:59:05Z',
               'continue' : '' }

num_revisions = 0

wp_call = requests.get(ENDPOINT, params=parameters)
response = wp_call.json()
print(response)

# look at the response: see 'continue'.
# this means there are more revisions than what we got in the response.

parameters['continue'] = response['continue']['continue']
parameters['rvcontinue'] = response['continue']['rvcontinue']

# do another call

wp_call = requests.get(ENDPOINT, params=parameters)
response = wp_call.json()
print(response)

# we can get all the revisions by looping until we don't see continue in the response any more
# introduce while loop
done = False
while not done:
    wp_call = requests.get(ENDPOINT, params=parameters)
    response = wp_call.json()
    print(response)
    
    # we need to copy the values the API gave us to continue
    if 'continue' in response:
        parameters['continue'] = response['continue']['continue']
        parameters['rvcontinue'] = response['continue']['rvcontinue']
    else:
        done = True
