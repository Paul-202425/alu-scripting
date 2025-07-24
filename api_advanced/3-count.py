#!/usr/bin/python3
"""
Recursive Reddit keyword counter for hot articles
"""
import requests
import re

def count_words(subreddit, word_list, word_count=None, after=None):
    if word_count is None:
        # Normalize and handle duplicates
        word_count = {}
        for word in word_list:
            w = word.lower()
            word_count[w] = word_count.get(w, 0)
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'cynt user agent 1.1'}
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False, timeout=10)
    except Exception:
        return  # Don't print anything on request failure

    if response.status_code != 200:
        return  # Don't print anything if subreddit is invalid

    data = response.json().get('data', {})
    posts = data.get('children', [])
    after = data.get('after', None)

    regexes = {w: re.compile(r'\b{}\b'.format(re.escape(w)), re.IGNORECASE) for w in word_count}

    for post in posts:
        title = post['data'].get('title', '')
        for w, regex in regexes.items():
            matches = regex.findall(title)
            word_count[w] += len(matches)

    if after:
        count_words(subreddit, word_list, word_count, after)
    else:
        # Filter and print only words that matched at least once
        filtered = [(k, v) for k, v in word_count.items() if v > 0]
        if not filtered:
            return  # Don't print anything if there are no matches
        # Sort: by count descending, then alphabetically
        for word, count in sorted(filtered, key=lambda x: (-x[1], x[0])):
            print(f"{word}: {count}")
