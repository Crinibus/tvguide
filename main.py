# from format import Format
# from argument import argparse_setup
# from API import API
# from Config import Config
import tvguide as tv


def print_currently_running(data_source: dict, user_channels: list) -> None:
    channels_string = ", ".join(user_channels).upper()

    print(f"\n----- Showing currently running programs for: {channels_string} -----", end="")
    for channel in user_channels:
        data_source[channel].print_currently_running()


def print_program_times(data_source: dict, user_channels: list, user_times: list) -> None:
    channels_string = ", ".join(user_channels).upper()
    user_times_string = ", ".join(user_times)

    print(f"\n----- Showing programs that is running at: {user_times_string} for: {channels_string} -----", end="")
    for channel in user_channels:
        data_source[channel].print_times(user_times)


def print_program_categories(data_source: dict, user_channels: list, user_categories: list) -> None:
    user_categories_string = ", ".join(user_categories)

    print(f"\n----- Searching for categories: {user_categories_string} -----", end="")
    for channel in user_channels:
        data_source[channel].print_categories(user_categories)


def print_program_searches(data_source: dict, user_channels: list, user_searches: list) -> None:
    user_search_string = tv.Format.user_search(", ".join(user_searches))

    print(f"\n----- Searching for keywords: {user_search_string} -----", end="")
    for channel in user_channels:
        data_source[channel].print_searches(user_searches)


def print_program_all(data_source: dict, user_channels: list) -> None:
    user_channels_string = ", ".join(user_channels).upper()

    print(f"\n----- Showing all programs for: {user_channels_string} -----", end="")
    for channel in user_channels:
        data_source[channel].print_all_programs()


def change_defaults(args, data: dict):
    if args.default_channels:
        tv.ConfigManager.change_defaults_user_channels(args.default_channels)
        default_channels_string = ", ".join(args.default_channels).upper()
        print(f"Changed default channel(s) to: {default_channels_string}")

    if args.default_space_seperator:
        tv.ConfigManager.change_space_seperator(args.default_space_seperator)
        print(f"Changed space seperator to: {args.default_space_seperator}")

    if args.justify_length:
        tv.ConfigManager.change_justify_length(args.justify_length)
        print(f"Changed justify length to: {args.justify_length}")

    if not args.channels:
        args.channels = tv.ConfigManager.get_defaults_user_channels()
        default_channels_string = ", ".join(args.channels).upper()
        print(f"No channel(s) chosen: using default channels ({default_channels_string})")
    elif args.channels[0].lower() == "all":
        args.channels = [channel for channel in data.keys()]


def print_programs(args, data):
    if args.now:
        print_currently_running(data, args.channels)

    if args.time:
        print_program_times(data, args.channels, args.time)

    if args.category:
        print_program_categories(data, args.channels, args.category)

    if args.search:
        print_program_searches(data, args.channels, args.search)

    if args.all:
        print_program_all(data, args.channels)


def main():
    args = tv.argparse_setup()

    api_data = tv.ApiManager.get_data(args.day)

    my_data = tv.ApiManager.format_data(api_data, args.verbose)

    change_defaults(args, my_data)

    print_programs(args, my_data)


if __name__ == "__main__":
    try:
        main()
    except KeyError:
        print("Check channel name or this scraper can't use this channel")
    except KeyboardInterrupt:
        print("Stopped by user")
