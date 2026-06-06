import requests
from django.core.cache import cache


def get_daily_affirmation():
    cached = cache.get('daily_affirmation')
    if cached:
        return cached
    try:
        r = requests.get('https://www.affirmations.dev/', timeout=5)
        if r.status_code == 200:
            text = r.json().get('affirmation', 'Find calm within.')
            cache.set('daily_affirmation', text, timeout=3600)
            return text
    except requests.RequestException:
        pass
    return 'Find calm within. You are enough.'


def get_quote_of_day():
    cached = cache.get('quote_of_day')
    if cached:
        return cached
    try:
        r = requests.get('https://zenquotes.io/api/today', timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data:
                quote = {
                    'text': data[0].get('q', ''),
                    'author': data[0].get('a', '')
                }
                cache.set('quote_of_day', quote, timeout=3600)
                return quote
    except requests.RequestException:
        pass
    return {'text': 'Peace comes from within.', 'author': 'Buddha'}