from datetime import datetime, timedelta, timezone
from const import API


class Format:
    @staticmethod
    def channel_name(name: str) -> str:
        name = name.replace("-", " ")
        return name.upper()

    @staticmethod
    def user_time(time: str) -> int:
        return int(time.replace(":", ""))

    @staticmethod
    def api_link(relative_date: int) -> str:
        return API.replace("{date}", Format.get_specified_date(relative_date))

    @staticmethod
    def get_specified_date(relative_date: int) -> str:
        """Convert relative date to real date, so that if argument 'relative_date' is 1, it get converted to tomorrow"""
        date = datetime.today()
        date += timedelta(days=relative_date)
        return date.strftime('%Y-%m-%d')

    @staticmethod
    def convert_unix_time(unix_time: int, toShow: bool):
        """Convert UNIX times to hour and minutes, e.g.: 1604692800 -> 2000 or 20:00\n
           Times are shifted from UTC to UTC+1 (CET)"""

        # TODO: Use datetime timezone to convert to my timezone

        time = datetime.utcfromtimestamp(unix_time)
        time += timedelta(hours=1)

        if toShow:
            return time.strftime('%H:%M')
        else:
            return int(time.strftime('%H%M'))


def get_api_link(relative_date: int) -> str:
    return Format.api_link(relative_date)
