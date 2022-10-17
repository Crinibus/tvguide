from typing import List
import argparse
from tvguide.config import ConfigManager

from tvguide.tv import Channel


class TvGuide:
    def __init__(self) -> None:
        self.show_all_channels = False
        self.input_channels: List[str] = []
        self.channels: List[Channel] = None

    def parse_arguments(self, args: argparse.Namespace) -> None:
        if args.default_channels:
            self._change_default_channels(args.default_channels)

        if args.default_space_seperator:
            self._change_default_space_seperator(args.default_space_seperator)

        if args.justify_length:
            self._change_default_justify_length(args.justify_length)

        if not args.channels:
            self.input_channels = self.get_default_channels()
        elif "all" in args.channels:
            self.show_all_channels = True
        else:
            self.input_channels = args.channels

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
