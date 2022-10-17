from typing import List
import argparse
from tvguide.config import ConfigManager

from tvguide.tv import Channel


class TvGuide:
    def __init__(self) -> None:
        self.relative_date = 0
        self.verbose = False
        self.show_now = False
        self.show_all_channels = False
        self.show_all_programs = False
        self.show_time = False
        self.input_time = None
        self.search = False
        self.input_channels: List[str] = []
        self.search_terms: List[str] = []
        self.channels: List[Channel] = []

    def parse_arguments(self, args: argparse.Namespace) -> None:
        self.verbose = args.verbose
        self.show_now = args.now
        self.relative_date = args.day
        self.show_all_programs = args.all
        self.search = args.search

        if args.default_channels:
            self._change_default_channels(args.default_channels)

        if args.default_space_seperator:
            self._change_default_space_seperator(args.default_space_seperator)

        if args.justify_length:
            self._change_default_justify_length(args.justify_length)

        if args.time:
            self.show_time = True
            self.input_time = args.time

        if not args.channels:
            self.input_channels = self.get_default_channels()
        elif "all" in args.channels:
            self.show_all_channels = True
        else:
            self.input_channels = args.channels

    def parse_api_data(self, api_data: dict) -> None:
        for channel_dict in api_data:
            channel = Channel(channel_dict, self.verbose)
            self.channels.append(channel)

    def print_programs(self) -> None:
        channels = self.get_channels(self.input_channels)

        for channel in channels:
            print(channel.name.upper())

    def get_channels(self, channel_names: List[str]) -> List[Channel]:
        return [channel for channel in self.channels if channel.name in channel_names]

    def _change_default_channels(self, channels: List[str]) -> None:
        ConfigManager.change_defaults_user_channels(channels)

    def _change_default_space_seperator(self, space_seperator: str) -> None:
        ConfigManager.change_space_seperator(space_seperator)

    def _change_default_justify_length(self, justify_length: int) -> None:
        ConfigManager.change_justify_length(justify_length)

    def get_default_channels(self) -> List[str]:
        return ConfigManager.get_defaults_user_channels()

    def get_default_space_seperator(self) -> str:
        return ConfigManager.get_space_seperator()

    def get_default_justify_length(self) -> int:
        return ConfigManager.get_justify_length()
