import json
import os

from oura_cdm.extract_oura import get_oura_data


if __name__ == '__main__':
    mocks_folder = 'mocks'
    out_file_name = 'mock_sleep_data.json'
    assert mocks_folder in os.listdir()
    raw_data = get_oura_data(start_date='2022-01-01', end_date='2022-02-01')
    assert len(raw_data) > 5
    with open(f'{mocks_folder}/{out_file_name}', 'w') as f:
        json.dump(raw_data, f)
    assert out_file_name in os.listdir(mocks_folder)
    with open(f'{mocks_folder}/{out_file_name}', 'r') as f:
        mock = json.load(f)
    assert mock == raw_data
