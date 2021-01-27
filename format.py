from datetime import datetime, timedelta, timezone
from configparser import ConfigParser
from const import API_LINK


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
           Times are shifted from UTC to UTC+1 (CET)"""

        # TODO: Use datetime timezone to convert to my timezone

        time = datetime.utcfromtimestamp(unix_time)
        time += timedelta(hours=1)

        if toShow:
            return time.strftime('%H:%M')
        else:
            return int(time.strftime('%H%M'))
    
    @staticmethod
    def user_search(search: str) -> str:
        search = search.lower()

        spaceSeperator  = Config.get_space_seperator()

        return search.replace(spaceSeperator, ' ')


class Api:
    @staticmethod
    def get_link(relative_date: int) -> str:
        return Api.format_link(relative_date)
    
    @staticmethod
    def format_link(relative_date: int) -> str:
        return API_LINK.replace("{date}", Format.get_specified_date(relative_date))


class Config:
    @staticmethod
    def read_config(file_name: str) -> ConfigParser:
        """Read user settings in {file_name}.ini"""
        config = ConfigParser()
        config.read(file_name)
        return config

    @staticmethod
    def write_config(file_name: str, config: ConfigParser) -> None:
        """Write user settings in {file_name}.ini"""
        with open(file_name, 'w') as default_file:
            config.write(default_file)

    @staticmethod
    def get_defaults_user_channels() -> list:
        config = Config.read_config('defaults.ini')

        defaultChannels = config['DefaultChannels']['channels']

        return defaultChannels.split(',')

    @staticmethod
    def change_defaults_user_channels(new_defaults: list) -> None:
        config = Config.read_config('defaults.ini')

        config['DefaultChannels']['channels'] = ','.join(new_defaults)

        Config.write_config('defaults.ini', config)
    
    @staticmethod
    def get_space_seperator() -> str:
        config = Config.read_config('defaults.ini')

        return config['Misc']['spaceSeperator']
    
    @staticmethod
    def change_space_seperator(new_space_seperator: str):
        config = Config.read_config('defaults.ini')

        config['Misc']['spaceSeperator'] = new_space_seperator

        Config.write_config('defaults.ini', config)
