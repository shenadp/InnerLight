import requests
from django.core.cache import cache
from django.utils import timezone

def get_daily_quote():
    today = timezone.now().date().isoformat()
    cache_key = f'zenquote_{today}'
    
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        response = requests.get(
            'https://zenquotes.io/api/random',
            timeout=5
        )
        data = response.json()
        quote = {
            'text': data[0]['q'],
            'author': data[0]['a'],
        }
    except Exception:
        quote = {
            'text': 'Every day is a new beginning.',
            'author': 'InnerLight',
        }

    cache.set(cache_key, quote, 60 * 60 * 24)
    return quote