from typing import List
from configparser import ConfigParser

from .filemanager import Filemanager


class ConfigManager:
    @staticmethod
    def read(file_name: str) -> ConfigParser:
        """Read user settings in {file_name}.ini"""
        config = ConfigParser()
        config.read(file_name)
        return config

    @staticmethod
    def write(file_name: str, config: ConfigParser) -> None:
        """Write user settings in {file_name}.ini"""
        with open(file_name, 'w') as default_file:
            config.write(default_file)

    @staticmethod
    def get_defaults_user_channels() -> List[str]:
        config = ConfigManager.read(Filemanager.defaults_ini_path)

        defaultChannels = config['DefaultChannels']['channels']

        return defaultChannels.split(',')

    @staticmethod
    def change_defaults_user_channels(new_defaults: List[str]) -> None:
        config = ConfigManager.read(Filemanager.defaults_ini_path)

        config['DefaultChannels']['channels'] = ','.join(new_defaults)

        ConfigManager.write(Filemanager.defaults_ini_path, config)

    @staticmethod
    def get_space_seperator() -> str:
        config = ConfigManager.read(Filemanager.defaults_ini_path)

        return config['Misc']['spaceSeperator']

    @staticmethod
    def change_space_seperator(new_space_seperator: str) -> None:
        config = ConfigManager.read(Filemanager.defaults_ini_path)

        config['Misc']['spaceSeperator'] = new_space_seperator

        ConfigManager.write(Filemanager.defaults_ini_path, config)

    @staticmethod
    def get_justify_length() -> int:
        config = ConfigManager.read(Filemanager.defaults_ini_path)

        return int(config['Misc']['justifyLength'])

    @staticmethod
    def change_justify_length(new_length: int):
        config = ConfigManager.read(Filemanager.defaults_ini_path)

        config['Misc']['justifyLength'] = new_length

        ConfigManager.write(Filemanager.defaults_ini_path, config)
