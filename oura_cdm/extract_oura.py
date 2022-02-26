import os
from datetime import date
from typing import Dict

import requests


def get_token() -> str:
    return os.environ['OURA_TOKEN']


def get_oura_data(token: str = None, start_date=None, end_date=None) -> Dict:
    if token is None:
        token = get_token()
    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")
    if start_date is None:
        start_date = '2000-02-01'
    url = f'https://api.ouraring.com/v1/sleep?start={start_date}&end={end_date}'
    ans = requests.get(url, params={"access_token": token}).json()
    return ans['sleep']
