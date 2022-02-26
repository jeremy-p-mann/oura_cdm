import json
import os
from datetime import date
from typing import Dict, List, Optional

import requests


def get_oura_token_environment_variable_name() -> str:
    return 'OURA_TOKEN'


def get_token() -> Optional[str]:
    token_name = get_oura_token_environment_variable_name()
    if token_name in os.environ.keys():
        return os.environ['OURA_TOKEN']
    return None


def _get_mock_oura_data() -> List[Dict]:
    with open('mocks/mock_sleep_data.json', 'rb') as f:
        ans = json.load(f)
    return ans


def get_oura_data(
    start_date=None,
    end_date=None
) -> List[Dict]:
    token = get_token()
    if token is None:
        return _get_mock_oura_data()
    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")
    if start_date is None:
        start_date = '2000-02-01'
    url = f'https://api.ouraring.com/v1/sleep?start={start_date}&end={end_date}'
    ans = requests.get(url, params={"access_token": token}).json()
    return ans['sleep']
