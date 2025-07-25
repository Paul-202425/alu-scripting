#!/usr/bin/python3
""" top_ten.py """
import requests


def top_ten(subreddit):
    url = 'https://www.reddit.com/r/{}/hot.json?limit=10'.format(subreddit)
    headers = {'User-Agent': 'myRedditScript/0.1 by u/Due-Memory4378'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        print("None")
        return
    posts = response.json().get('data', {}).get('children', [])
    if not posts:
        return  # Don't print anything for empty posts!
    for post in posts:
        title = post['data'].get('title')
        if title:  # Extra guard
            print(title)
