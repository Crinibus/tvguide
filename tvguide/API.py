import requests
from .const import API_LINK, REQUEST_HEADER, REQUEST_COOKIES
from .format import Format
from .tv import Channel


class API:
    @staticmethod
    def get_link(relative_date: int) -> str:
        return API_LINK.replace("{date}", Format.get_specified_date(relative_date))

    @staticmethod
    def get_data(relative_day: int) -> dict:
        """Get formatted data from API"""
        response = requests.get(
            API.get_link(relative_day),
            headers=REQUEST_HEADER,
            cookies=REQUEST_COOKIES
        )

        return response.json()

    @staticmethod
    def format_data(api_data: dict, verbose: bool) -> dict:
        formatted_data = {}

        for channel in api_data:
            temp_channel = Channel(channel, verbose)
            formatted_data.update({temp_channel.name: temp_channel})

        return formatted_data
