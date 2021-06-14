import json, os
from datetime import datetime
from app.data import cache

import requests

@cache.cached(timeout=50, key_prefix='banxico_parse_today')
def parse_today():
    banxico_token = os.environ.get('BANXICO_TOKEN')
    url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno?token={}'\
        .format(banxico_token)
    data = json.loads(requests.get(url).text)
    if not data:
        return None

    series = data.get('bmx', {}).get('series')
    if not series:
        return None

    serie = series[0]
    datum = serie.get('datos')
    if not datum:
        return None

    date = datetime.strptime(datum[0].get('fecha'), '%d/%m/%Y')
    value = datum[0].get('dato')

    return date, float(value)



if __name__ == '__main__':
    print(parse_today())