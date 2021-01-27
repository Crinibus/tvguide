import requests
from argparse import ArgumentParser
from datetime import datetime
import json # only used for argument and return type indicator
from const import *
from format import *


def argparse_setup() -> ArgumentParser.parse_args:
    """Setup and return argparse."""
    parser = ArgumentParser()

    parser.add_argument(
        '-c',
        '--channel',
        dest='channel',
        help='the channel with the user want to see programs from',
        action='append',
        type=str
    )

    parser.add_argument(
        '-t',
        '--time',
        dest='time',
        metavar='hh:mm',
        help='the time the program starts. E.g. "20:00". Format is: "hh:mm"',
        action='append',
        type=str
    )

    parser.add_argument(
        '-a',
        '--all',
        help='show all programs for the chosen channel(s)',
        action='store_true'
    )

    parser.add_argument(
        '-d',
        '--day',
        help='the relative day the programs is running, default today (0)',
        choices=[-1, 0, 1, 2, 3, 4, 5, 6],
        type=int,
        default=0
    )

    parser.add_argument(
        '--category',
        dest='category',
        help='only show the programs with the chosen category(s)',
        action='append',
        type=str
    )

    parser.add_argument(
        '-n',
        '--now',
        help='only show the program(s) that is currently',
        action='store_true'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        help='show categories when using --all and --time',
        action='store_true'
    )

    parser.add_argument(
        '--default-channels',
        dest='default_channels',
        help='change default channels to the chosen channel(s)',
        nargs='*'
    )

    parser.add_argument(
        '--default-space-seperator',
        dest='default_space_seperator',
        help='change space seperator sign',
        type=str
    )

    parser.add_argument(
        '-s',
        '--search',
        dest='search',
        help='search for programs',
        action='append',
        type=str
    )

    return parser.parse_args()


class Program:
    def __init__(self, program_info: json):
        self.info = program_info
        self.format_info()

    def format_info(self):
        self.time_start_unix = self.info['start']
        self.time_stop_unix = self.info['stop']
        self.time_start = Format.convert_unix_time(self.time_start_unix, toShow=False)
        self.time_stop = Format.convert_unix_time(self.time_stop_unix, toShow=False)
        self.time_start_show = Format.convert_unix_time(self.time_start_unix, toShow=True)
        self.time_stop_show = Format.convert_unix_time(self.time_stop_unix, toShow=True)
        self.title = self.info['title']
        self.categories = [cat.lower() for cat in self.info['categories']]

    @property
    def time_and_title(self) -> str:
        if args.verbose:
            return self.time_and_title_and_category
        
        return f"{self.time_start_show} - {self.time_stop_show} > {self.title}"

    @property
    def start_time_and_title(self) -> str:
        if args.verbose:
            return f"{self.time_start_show} > {self.title} \t ({', '.join(self.categories)})"

        return f"{self.time_start_show} > {self.title}"

    @property
    def time_and_title_and_category(self) -> str:
        return f"{self.time_start_show} - {self.time_stop_show} > {self.title} \t ({', '.join(self.categories)})"


def get_data() -> json:
    response = requests.get(
        Api.get_api_link(args.day),
        headers=REQUEST_HEADER,
        cookies=REQUEST_COOKIES
    )

    return format_data(response.json())


def format_data(data: json) -> json:
    formatted_data = {}

    for channel in data:
        for program in channel['programs']:
            add_program_to_dict(formatted_data, channel['id'], Program(program))
    
    return formatted_data


def add_program_to_dict(data_dict: dict, channel_id: str, program: Program) -> None:
    channel_name = CHANNEL_NUMBER_INDEX[channel_id]

    if channel_name not in data_dict.keys():
        data_dict.update({channel_name: []})

    data_dict[channel_name].append(program)


def print_all_channels_all_programs(data_source: dict) -> None:
    for channel in data_source.keys():
        print(f"\n{Format.channel_name(channel)}:")
        for program in data_source[channel]:
            print(program.start_time_and_title)
        print()


def print_one_channel_all_programs(data_source: dict, channel_name: str) -> None:
    print(f"\n{Format.channel_name(channel_name)}:")
    for program in data_source[channel_name]:
        print(program.start_time_and_title)
    print()


def print_user_channels_all_programs(data_source: dict, user_channels: list) -> None:
    for user_channel in user_channels:
        print(f"\n{Format.channel_name(user_channel)}:")
        for program in data_source[user_channel]:
            print(program.start_time_and_title)
        print()


def print_all_channels_programs_user_times(data_source: dict, user_times: list) -> None:
    for user_time in user_times:
        user_time = Format.user_time(user_time)

        for channel in data_source.keys():
            print(f"\n{Format.channel_name(channel)}:")
            for program in data_source[channel]:
                if user_time == program.time_start:
                    print(program.time_and_title)
                    break
                elif program.time_start < user_time and program.time_stop > user_time:
                    print(program.time_and_title)
                    break
            print()


def print_user_channels_programs_user_times(data_source: dict, user_channels: list, user_times: list) -> None:
    for user_channel in user_channels:
        print(f"\n{Format.channel_name(user_channel)}:")
        for program in data_source[user_channel]:
            for user_time in user_times:
                user_time = Format.user_time(user_time)
                if user_time == program.time_start:
                    print(program.time_and_title)
                    break
                elif user_time > program.time_start and user_time < program.time_stop:
                    print(program.time_and_title)
                    break
        print()


def print_all_channels_all_programs_user_times(data_source: dict, user_times: list) -> None:
    for channel in data_source.keys():
        print(f"\n{Format.channel_name(channel)}:")
        for program in data_source[channel]:
            for user_time in user_times:
                user_time = Format.user_time(user_time)
                if user_time == program.time_start:
                    print(program.time_and_title)
                    break
                elif program.time_start < user_time and program.time_stop > user_time:
                    print(program.time_and_title)
                    break
        print()


def print_user_channels_programs_user_categories(data_source: dict, user_channels: list, user_categories: list) -> None:
    for user_channel in user_channels:
        print(f"\n{Format.channel_name(user_channel)}:")
        for program in data_source[user_channel]:
            for user_cat in user_categories:
                user_cat = user_cat.lower()
                if user_cat in program.categories:
                    print(f"{program.time_and_title} ({user_cat.capitalize()})")
                    break
                elif program.categories == [] and user_cat in ['nyheder']:
                    print(f"{program.time_and_title} ({user_cat.capitalize()})")
                    break
        print()


def print_user_channels_program_currently_running(data_source: dict, user_channels: list) -> None:
    time = datetime.now()
    time_current = time.strftime('%H:%M')
    print_user_channels_programs_user_times(data_source, user_channels, [time_current])


def print_user_channels_programs_search(data_source: dict, user_channels: list, user_searches: list) -> None:
    for user_channel in user_channels:
        print(f"\n{Format.channel_name(user_channel)}:")
        for program in data_source[user_channel]:
            for user_search in user_searches:
                user_search = Format.user_search(user_search)
                if user_search in program.title.lower():
                    print(program.time_and_title)
        print()


def main(args):
    my_data = get_data()

    if args.default_channels:
        Config.change_defaults_user_channels(args.default_channels)
        print(f"Changed default channel(s) to: {', '.join(args.default_channels)}")

    if args.default_space_seperator:
        Config.change_space_seperator(args.default_space_seperator)
        print(f"Changed space seperator to: {args.default_space_seperator}")

    if not args.channel:
        args.channel = Config.get_defaults_user_channels()
        print(f"No channel(s) chosen: using default channels ({', '.join(args.channel)})")
    elif args.channel[0].lower() == 'all':
        args.channel = [channel for channel in my_data.keys()]

    if args.now:
        print_user_channels_program_currently_running(my_data, args.channel)

    if args.time:
        print_user_channels_programs_user_times(my_data, args.channel, args.time)

    if args.category:
        print_user_channels_programs_user_categories(my_data, args.channel, args.category)

    if args.search:
        print_user_channels_programs_search(my_data, args.channel, args.search)

    if args.all:
        print_user_channels_all_programs(my_data, args.channel)


if __name__ == "__main__":
    args = argparse_setup()

    try:
        main(args)
    except KeyError:
        print("Check channel name or this scraper can't use this channel")
    except KeyboardInterrupt:
        print("Stopped by user")
