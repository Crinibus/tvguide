import requests
import requests_cache
from .const import API_LINK, REQUEST_HEADER, REQUEST_COOKIES
from .format import Format
from .tv import Channel

requests_cache.install_cache(cache_name="api_cache", expire_after=120, backend="filesystem")


class ApiManager:
    @staticmethod
    def get_link(relative_date: int) -> str:
        date = Format.get_specified_date(relative_date)
        return API_LINK.replace("{date}", date)

    @staticmethod
    def get_data(relative_day: int) -> dict:
        """Get formatted data from API"""
        api_link = ApiManager.get_link(relative_day)
        response = requests.get(api_link, headers=REQUEST_HEADER, cookies=REQUEST_COOKIES)

        return response.json()

    @staticmethod
    def format_data(api_data: dict, verbose: bool) -> dict:
        formatted_data = {}

        for channel in api_data:
            temp_channel = Channel(channel, verbose)
            formatted_data.update({temp_channel.name: temp_channel})

        return formatted_data
