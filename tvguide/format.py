from datetime import datetime, timedelta, timezone
from .config import ConfigManager
import pytz


class Format:
    @staticmethod
    def channel_name(name: str) -> str:
        name = name.replace("-", " ")
        return name.upper()

    @staticmethod
    def user_time(time: str) -> int:
        return int(time.replace(":", ""))

    @staticmethod
    def get_specified_date(relative_date: int) -> str:
        """Convert relative date to real date, so that if argument 'relative_date' is 1, it get converted to tomorrow"""
        date = datetime.today()
        date += timedelta(days=relative_date)
        return date.strftime('%Y-%m-%d')

    @staticmethod
    def convert_unix_time(unix_time: int, toShow: bool):
        """Convert UNIX times to hour and minutes, e.g.: 1604692800 -> 2000 or 20:00\n
           UNIX time is converted to timezone: Europe/Copenhagen"""

        copenhagen_timezone = pytz.timezone("Europe/Copenhagen")
        time = pytz.utc.localize(datetime.utcfromtimestamp(unix_time)).astimezone(copenhagen_timezone)

        if toShow:
            return time.strftime('%H:%M')
        else:
            return int(time.strftime('%H%M'))

    @staticmethod
    def user_search(search: str) -> str:
        search = search.lower()

        spaceSeperator  = ConfigManager.get_space_seperator()

        return search.replace(spaceSeperator, ' ')
    
    @staticmethod
    def program_time_stop(time_start: int, time_stop: int) -> int:
        if time_start > time_stop:
            return 2400 + time_stop

        return time_stop
