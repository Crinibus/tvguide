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
        self.search_times = False
        self.search_categories = False
        self.search_names = False
        self.input_times: List[str] = []
        self.input_channels: List[str] = []
        self.input_categories: List[str] = []
        self.input_search_terms: List[str] = []
        self.channels: List[Channel] = []

    def parse_arguments(self, args: argparse.Namespace) -> None:
        self.verbose = args.verbose
        self.show_now = args.now
        self.relative_date = args.day
        self.show_all_programs = args.all

        if args.default_channels:
            self._change_default_channels(args.default_channels)

        if args.justify_length:
            self._change_default_justify_length(args.justify_length)

        if args.search:
            self.search_names = True
            self.input_search_terms = args.search

        if args.category:
            self.search_categories = True
            self.input_categories = args.category

        if args.time:
            self.search_times = True
            self.input_times = args.time

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
        channels = self.channels if self.show_all_channels else self.get_channels(self.input_channels)

        for channel in channels:
            print(f"\n{channel.name.upper()}")

            if self.show_all_programs:
                print("----- ALL -----")
                channel.print_all_programs()
                print()

            if self.search_categories:
                print("----- CATEGORY -----")
                channel.print_categories(self.input_categories)
                print()

            if self.search_times:
                print("----- TIMES -----")
                channel.print_times(self.input_times)
                print()

            if self.search_names:
                print("----- SEARCH -----")
                channel.print_searches(self.input_search_terms)
                print()

            if self.show_now:
                print("----- NOW -----")
                channel.print_currently_running()
                print()

    def get_channels(self, channel_names: List[str]) -> List[Channel]:
        return [channel for channel in self.channels if channel.name in channel_names]

    def _change_default_channels(self, channels: List[str]) -> None:
        ConfigManager.change_defaults_user_channels(channels)

    def _change_default_justify_length(self, justify_length: int) -> None:
        ConfigManager.change_justify_length(justify_length)

    def get_default_channels(self) -> List[str]:
        return ConfigManager.get_defaults_user_channels()

    def get_default_justify_length(self) -> int:
        return ConfigManager.get_justify_length()
