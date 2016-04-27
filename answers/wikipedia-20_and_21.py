# Copyright (C) 2016 Ben Lewis, and Morten Wang
# Licensed under the MIT license, see ../LICENSE

import requests
from urllib.parse import quote

# Notes:
# 1: documentation https://wikimedia.org/api/rest_v1/?doc
# 2: there is no view data for 20160403, bug?

ENDPOINT = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/'

wp_code = 'en.wikipedia'
access = 'all-access'
agents = 'all-agents'
page_title = 'Panama Papers'
period = 'daily'
start_date = '20160404'
end_date = '20160423'

wp_call = requests.get(ENDPOINT + wp_code + '/' + access + '/' + agents + '/' + quote(page_title, safe='') + '/' + period + '/' + start_date + '/' + end_date)
response = wp_call.json()

total_views = 0
days = 23-4
for item in response['items']:
    total_views = total_views + item['views']

views_per_day = total_views / days
print(page_title + ' had ' + str(views_per_day) + ' views per day')
