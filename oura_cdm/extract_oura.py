import json
import os
from datetime import date
from typing import Dict, List, Optional
from functools import partial

import requests

from oura_cdm.logs import log_info, log_warning


log_info_e = partial(log_info, **{'name': __name__})
log_warning_e = partial(log_warning, **{'name': __name__})


def get_oura_token_environment_variable_name() -> str:
    return 'OURA_TOKEN'


def get_token() -> Optional[str]:
    token_name = get_oura_token_environment_variable_name()
    if token_name in os.environ.keys():
        return os.environ['OURA_TOKEN']
    return None


def _get_mock_oura_data() -> List[Dict]:
    mock_data_folder = 'mocks/mock_sleep_data.json'
    log_info_e(f'Getting mock data from {mock_data_folder}')
    with open(mock_data_folder, 'rb') as f:
        ans = json.load(f)
    return ans


def get_oura_data(
    start_date=None,
    end_date=None
) -> List[Dict]:
    token = get_token()
    if token is None:
        log_warning_e('No token provided running pipeline on mock data')
        return _get_mock_oura_data()
    if end_date is None:
        end_date = date.today().strftime("%Y-%m-%d")
    if start_date is None:
        start_date = '2000-02-01'
    log_info_e(f'Getting data from oura from {start_date} to {end_date}')
    url = f'https://api.ouraring.com/v1/sleep?start={start_date}&end={end_date}'
    ans = requests.get(url, params={"access_token": token})
    if ans.status_code == 401:
        log_warning_e('No token provided running pipeline on mock data')
        return _get_mock_oura_data()[:0]
    ans = ans.json()
    log_info_e('Oura query successful')
    return ans['sleep']
