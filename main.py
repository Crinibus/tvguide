# from format import Format
# from argument import argparse_setup
# from API import API
# from Config import Config
import tvguide as tv


def print_currently_running(data_source: dict, user_channels: list) -> None:
    print(f"\n----- Showing currently running programs for: {', '.join(user_channels).upper()} -----", end='')
    for channel in user_channels:
        data_source[channel].print_currently_running()


def print_program_times(data_source: dict, user_channels: list, user_times: list) -> None:
    print(f"\n----- Showing programs that is running at: {', '.join(user_times)} for: {', '.join(user_channels).upper()} -----", end='')
    for channel in user_channels:
        data_source[channel].print_times(user_times)


def print_program_categories(data_source: dict, user_channels: list, user_categories: list) -> None:
    print(f"\n----- Searching for categories: {', '.join(user_categories)} -----", end='')
    for channel in user_channels:
        data_source[channel].print_categories(user_categories)


def print_program_searches(data_source: dict, user_channels: list, user_searches: list) -> None:
    print(f"\n----- Searching for keywords: {tv.Format.user_search(', '.join(user_searches))} -----", end='')
    for channel in user_channels:
        data_source[channel].print_searches(user_searches)


def print_program_all(data_source: dict, user_channels: list) -> None:
    print(f"\n----- Showing all programs for: {', '.join(user_channels).upper()} -----", end='')
    for channel in user_channels:
        data_source[channel].print_all_programs()


def main(args):
    api_data = tv.API.get_data(args.day)

    my_data = tv.API.format_data(api_data, args.verbose)

    if args.default_channels:
        tv.Config.change_defaults_user_channels(args.default_channels)
        print(f"Changed default channel(s) to: {', '.join(args.default_channels).upper()}")

    if args.default_space_seperator:
        tv.Config.change_space_seperator(args.default_space_seperator)
        print(f"Changed space seperator to: {args.default_space_seperator}")

    if args.justify_length:
        tv.Config.change_justify_length(args.justify_length)
        print(f"Changed justify length to: {args.justify_length}")

    if not args.channel:
        args.channel = tv.Config.get_defaults_user_channels()
        print(f"No channel(s) chosen: using default channels ({', '.join(args.channel).upper()})")
    elif args.channel[0].lower() == 'all':
        args.channel = [channel for channel in my_data.keys()]

    if args.now:
        print_currently_running(my_data, args.channel)

    if args.time:
        print_program_times(my_data, args.channel, args.time)

    if args.category:
        print_program_categories(my_data, args.channel, args.category)

    if args.search:
        print_program_searches(my_data, args.channel, args.search)

    if args.all:
        print_program_all(my_data, args.channel)


if __name__ == "__main__":
    args = tv.argparse_setup()

    try:
        main(args)
    except KeyError:
        print("Check channel name or this scraper can't use this channel")
    except KeyboardInterrupt:
        print("Stopped by user")
