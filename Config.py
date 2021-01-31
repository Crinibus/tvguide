from configparser import ConfigParser


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
    def change_space_seperator(new_space_seperator: str) -> None:
        config = Config.read_config('defaults.ini')

        config['Misc']['spaceSeperator'] = new_space_seperator

        Config.write_config('defaults.ini', config)

    @staticmethod
    def get_justify_length() -> int:
        config = Config.read_config('defaults.ini')

        return int(config['Misc']['justifyLength'])

    @staticmethod
    def change_justify_length(new_length: int):
        config = Config.read_config('defaults.ini')

        config['Misc']['justifyLength'] = new_length

        Config.write_config('defaults.ini', config)
