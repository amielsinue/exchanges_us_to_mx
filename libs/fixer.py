import json, os
import requests
import pytz
from datetime import datetime
from app.data import cache


@cache.cached(timeout=50, key_prefix='fixer_parse_today')
def parse_today():
    fixer_access_key = os.environ.get('FIXER_ACCESS_KEY')
    url = 'http://data.fixer.io/api/latest?access_key={}&format=1&base=EUR'.format(fixer_access_key)
    data = json.loads(requests.get(url).text)
    if not data:
        return None
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    try:
        date = pytz.timezone('Europe/Madrid').localize(date, is_dst=None)
        date = date.astimezone(pytz.timezone('America/Mexico_City'))
    except:
        return None

    rates = data.get('rates')
    if not rates:
        return None

    mxn = rates.get('MXN')
    usd = rates.get('USD')
    if not mxn or not usd:
        return None

    return date, (mxn / usd)


if __name__ == '__main__':
    print(parse_today())
