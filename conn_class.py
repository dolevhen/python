import requests
import json
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class NYCData:
    COUNT_QUERY = {'$select': 'COUNT(*)'}
    DEFAULT_CHUNK_SIZE = 100000

    def __init__(self, data_url):
        self.data_url = data_url

    def _get_count(self):
        count_response = requests.get(self.data_url, params=self.COUNT_QUERY)
        count_data = json.loads(count_response.text)
        return int(count_data[0]['COUNT'])

    def _validate_count(self, count):
        if count == 0:
            logger.warning("No data found at the provided URL.")
            raise ValueError("No data found")
