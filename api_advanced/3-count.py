#!/usr/bin/python3
"""
Recursive Reddit keyword counter for hot articles
"""
import requests
import re

def count_words(subreddit, word_list, word_count=None, after=None):
    if word_count is None:
        # Normalize word list to lowercase, and sum counts for duplicates
        word_count = {}
        for word in word_list:
            w = word.lower()
            word_count[w] = word_count.get(w, 0) + 0  # initialize at 0

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'cynt user agent 1.1'}
    params = {'limit': 100}
    if after:
        params['after'] = after

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    if response.status_code != 200:
        return

    data = response.json().get('data', {})
    posts = data.get('children', [])
    after = data.get('after', None)

    # Compile regex for each word in word_list for word boundaries, case-insensitive
    regexes = {w: re.compile(r'\b{}\b'.format(re.escape(w)), re.IGNORECASE) for w in word_count}

    for post in posts:
        title = post['data'].get('title', '')
        for w, regex in regexes.items():
            matches = regex.findall(title)
            word_count[w] += len(matches)

    if after:
        # More posts, so recurse
        return count_words(subreddit, word_list, word_count, after)
    else:
        # Print results sorted as required
        filtered = {k: v for k, v in word_count.items() if v > 0}
        if not filtered:
            return
        # Sort: by count descending, then alphabetically ascending
        sorted_words = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_words:
            print(f"{word}: {count}")


