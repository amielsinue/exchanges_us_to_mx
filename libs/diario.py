import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from app.data import cache


@cache.cached(timeout=50, key_prefix='diario_parse_today')
def parse_today():
    vgm_url = 'https://www.banxico.org.mx/tipcamb/tipCamMIAction.do'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    tables = soup.find_all('table')
    # table_rows
    tds_values = soup.find_all('td', string=re.compile(r'^\s+([0-9]+\.[0-9]+)\s+$'))
    tds_dates = soup.find_all('td', string=re.compile(r'^\s+([0-9]{2}\/[0-9]{2}/[0-9]{4})\s+$'))
    if not tds_values or not tds_dates:
        return None

    value_match = re.search(r'^\s+([0-9]+\.[0-9]+)\s+$', tds_values[0].get_text())
    date_match = re.search(r'^\s+([0-9]{2}\/[0-9]{2}/[0-9]{4})\s+$', tds_dates[0].get_text())
    if not value_match or not date_match:
        return None

    value = value_match.group(1)
    date = datetime.strptime(date_match.group(1), '%d/%m/%Y')

    return date, float(value)


if __name__ == '__main__':
    print(parse_today())
