import requests
import argparse
from datetime import datetime
import json # only used for argument and return type indicator
from const import *
from format import Format, get_api_link


def argparse_setup():
    """Setup and return argparse."""
    parser = argparse.ArgumentParser()

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

    return parser.parse_args()


class Program:
    def __init__(self, program_info: json):
        self.info = program_info
        self.format_info()

    def format_info(self):
        self.time_start_unix = self.info["start"]
        self.time_stop_unix = self.info["stop"]
        self.time_start = Format.convert_unix_time(self.time_start_unix, toShow=False)
        self.time_stop = Format.convert_unix_time(self.time_stop_unix, toShow=False)
        self.time_start_show = Format.convert_unix_time(self.time_start_unix, toShow=True)
        self.time_stop_show = Format.convert_unix_time(self.time_stop_unix, toShow=True)
        self.title = self.info["title"]
        self.categories = [cat.lower() for cat in self.info["categories"]]

    @property
    def time_and_title(self) -> str:
        if not args.verbose:
            return f"{self.time_start_show} - {self.time_stop_show} > {self.title}"
        else:
            return self.time_and_title_and_category

    @property
    def start_time_and_title(self) -> str:
        if not args.verbose:
            return f"{self.time_start_show} > {self.title}"
        else:
            return f"{self.time_start_show} > {self.title} \t ({', '.join(self.categories)})"

    @property
    def time_and_title_and_category(self) -> str:
        return f"{self.time_start_show} - {self.time_stop_show} > {self.title} \t ({', '.join(self.categories)})"


def get_data() -> json:
    response = requests.get(
        get_api_link(args.day),
        headers=REQUEST_HEADER,
        cookies=REQUEST_COOKIES
    )

    return response.json()


def format_data():
    data = get_data()
    for channel in data:
        for program in channel["programs"]:
            add_program_to_my_data(channel["id"], Program(program))


def add_program_to_my_data(channel_id: str, program: Program):
    channel_name = CHANNEL_NUMBER_INDEX[channel_id]

    if channel_name not in my_data.keys():
        my_data.update({channel_name: []})

    my_data[channel_name].append(program)


def print_all_programs():
    for channel in my_data.keys():
        print(f"\n{Format.channel_name(channel)}:")
        for program in my_data[channel]:
            print(program.start_time_and_title)
        print()


def print_one_channel(channel_name: str):
    print(f"\n{Format.channel_name(channel_name)}:")
    for program in my_data[channel_name]:
        print(program.start_time_and_title)
    print()


def print_channels_all_programs(user_channels: list):
    for user_channel in user_channels:
        print(f"\n{Format.channel_name(user_channel)}:")
        for program in my_data[user_channel]:
            print(program.start_time_and_title)
        print()


def print_program_time(user_times: list):
    for user_time in user_times:
        user_time = Format.user_time(user_time)

        for channel in my_data.keys():
            print(f"\n{Format.channel_name(channel)}:")
            for program in my_data[channel]:
                if user_time == program.time_start:
                    print(program.time_and_title)
                    break
                elif program.time_start < user_time and program.time_stop > user_time:
                    print(program.time_and_title)
                    break
            print()


def print_channel_program_time(user_channels: list, user_times: list):
    for user_channel in user_channels:
        print(f"\n{Format.channel_name(user_channel)}:")
        for program in my_data[user_channel]:
            for user_time in user_times:
                user_time = Format.user_time(user_time)
                if user_time == program.time_start:
                    print(program.time_and_title)
                    break
                elif user_time > program.time_start and user_time < program.time_stop:
                    print(program.time_and_title)
                    break
        print()


def print_channel_all_program_time(user_times: list):
    for channel in my_data.keys():
        print(f"\n{Format.channel_name(channel)}:")
        for program in my_data[channel]:
            for user_time in user_times:
                user_time = Format.user_time(user_time)
                if user_time == program.time_start:
                    print(program.time_and_title)
                    break
                elif program.time_start < user_time and program.time_stop > user_time:
                    print(program.time_and_title)
                    break
        print()


def print_programs_categories(user_channels: list, user_categories: list):
    for user_channel in user_channels:
        print(f"\n{Format.channel_name(user_channel)}:")
        for program in my_data[user_channel]:
            for user_cat in user_categories:
                user_cat = user_cat.lower()
                if user_cat in program.categories:
                    print(f"{program.time_and_title} ({user_cat.capitalize()})")
                    break
                elif program.categories == [] and user_cat in ["nyheder"]:
                    print(f"{program.time_and_title} ({user_cat.capitalize()})")
                    break
        print()


def print_program_currently(user_channels: list):
    time = datetime.now()
    time_current = time.strftime("%H:%M")
    print_channel_program_time(args.channel, [time_current])


def main(args):
    format_data()

    if not args.channel:
        args.channel = ['dr1', 'tv2']
        print('No channel(s) chosen: using default channels (dr1, tv2)')
    elif args.channel[0].lower() == 'all':
        args.channel = [channel for channel in my_data.keys()]

    if args.now:
        print_program_currently(args.channel)

    if args.time:
        print_channel_program_time(args.channel, args.time)

    if args.category:
        print_programs_categories(args.channel, args.category)

    if args.all:
        print_channels_all_programs(args.channel)


if __name__ == "__main__":
    my_data = {}
    args = argparse_setup()
    try:
        main(args)
    except KeyError:
        print("Check channel name or this scraper can't use this channel")
    except KeyboardInterrupt:
        print("Stopped by user")
