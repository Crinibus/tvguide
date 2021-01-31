import requests
from const import API_LINK, REQUEST_HEADER, REQUEST_COOKIES
from format import Format


class API:
    @staticmethod
    def get_link(relative_date: int) -> str:
        return API.format_link(relative_date)

    @staticmethod
    def format_link(relative_date: int) -> str:
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
