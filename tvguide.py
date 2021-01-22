import requests
import argparse
from datetime import datetime, timedelta, timezone
import validate_arguments as validate_args


def argparse_setup():
    """Setup and return argparse."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c',
        '--channel',
        help='the channel with the user want to see programs from',
        action='append',
        type=str
    )

    parser.add_argument(
        '-t',
        '--time',
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
        help='the date/day the programs is running, default today (0)',
        type=validate_args.validate_date_argument,
        default=0
    )

    parser.add_argument(
        '--category',
        help='only show the programs with the chosen category(s)',
        action='append',
        type=str
    )

    return parser.parse_args()


def get_specified_date(relative_date: int):
    """Convert relative date to real date, so that if argument 'relative_date' is 1, it get converted to tomorrow"""
    date = datetime.today()
    date += timedelta(days=relative_date)
    date = date.strftime('%Y-%m-%d')
    return date


def get_data():
    date = get_specified_date(args.day)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
    cookies = dict(cookies_are='working')
    response = requests.get(f'https://tvtid-api.api.tv2.dk/api/tvtid/v1/epg/dayviews/2021-01-22?ch=1&ch=2&ch=3&ch=4&ch=5&ch=6&ch=7&ch=8&ch=9&ch=10&ch=11&ch=12&ch=14&ch=15&ch=19&ch=20&ch=25&ch=26&ch=31&ch=37&ch=39&ch=70&ch=71&ch=74&ch=77&ch=93&ch=94&ch=111&ch=116&ch=117&ch=117&ch=118&ch=129&ch=130&ch=133&ch=135&ch=136&ch=142&ch=147&ch=153&ch=156&ch=157&ch=161&ch=162&ch=163&ch=164&ch=165&ch=174&ch=181&ch=185&ch=188&ch=191&ch=201&ch=215&ch=218&ch=219&ch=221&ch=240&ch=248&ch=570&ch=687&ch=689&ch=10061&ch=10066&ch=10070&ch=10093&ch=10104&ch=10111&ch=10145&ch=10153&ch=10159&ch=10262&ch=10341&ch=10435&ch=10455&ch=10510&ch=10511&ch=10621&ch=11572&ch=11610&ch=11611&ch=11612&ch=11613&ch=11614&ch=11615&ch=11616&ch=11617&ch=12034&ch=12396&ch=12566&ch=12697&ch=12948&ch=15032&ch=15049&ch=15129&ch=2147483561&ch=2147483566&ch=2147483567&ch=2147483568',
                            headers=headers,
                            cookies=cookies)

    return response.json()


def get_channels() -> list:
    """Get data from all channels"""
    data = get_data()
    return data


def get_programs(channel_list: list, user_channels: list) -> dict:
    """Find the programs for the specified channels and return a dict with them where the channels are the keys"""
    channel_index = {
        'dr1': 1,
        'tv2': 3,
        'tv3': 5,
        'dr2': 2,
        'tv2-charlie': 31,
        'tv2-news': 133,
        'kanal-5': 7,
        'tv3-plus': 6,
        'tv2-zulu': 4,
        'dr-ramasjang': 10153,
        'kanal-4': 8,
        'tv2-sport': 77,
        'tv2-sport-x': 2147483561,
        'tv3-sport': 156,
        'tv3-puls': 10093,
        '6eren': 10066,
        'disney-channel': 14,
        'tv2-fri': 12566,
        'canal-9': 10111,
        'discovery-channel': 70,
        'tlc': 118,
        'nickelodeon': 153,
        'national-geographic-channel': 94,
        'tv3-max': 12948,
        'cartoon': 185,
        'disney-junior': 157,
        'dk4': 15,
        'mtv': 71,
        'animal-planet': 93,
        'investigation-discovery': 15049,
        'vh1': 219,
        'eurosport-2': 37,
        'boomerang': 248,
        'viasat-film': 9,
        'viasat-film-action': 10,
        'viasat-film-hits': 11,
        'viasat-film-family': 12,
        'viasat-explorer': 19,
        'viasat-nature': 20,
        'c-more-first': 25,
        'c-more-hits': 26,
        'viasat-history': 39,
        'disney-xd': 74,
        'tv4-sverige': 111,
        'discovery-world': 116,
        'nrk2': 129,
        'nrk1': 130,
        'svt1': 135,
        'sv2': 136,
        'tv2-norge': 142,
        'discovery-hd-showcase': 147,
        'rtl': 161,
        'ard': 162,
        'zdf': 163,
        '3sat': 164,
        'viasat-golf': 165,
        'eurosport-1': 174,
        'cnn': 181,
        'ndr': 188,
        'bbc-world': 191,
        'c-more-series': 201,
        'travel-channel': 215,
        'vox': 218,
        'rtl-2': 221,
        'super-rtl': 240,
        'paramount-network': 570,
        'xee': 687,
        'viasat-ultra': 689,
        'bbc-earth': 10061,
        'viasat-series': 10070,
        'arte': 10104,
        'sf-kanalen': 10145,
        'history': 10159,
        'kanal-hovedstaden': 10262,
        'folketinget': 10341,
        'tnt': 10435,
        'nickelodeon-junior': 10455,
        'sat1': 10510,
        'prosieben': 10511,
        'sport1': 10621,
        'national-geographic-wild': 11572,
        'tv2-nord-salto': 11610,
        'tv-midt-vest': 11611,
        'tv2-østjylland': 11612,
        'tv2-øst': 11613,
        'tv-syd': 11614,
        'tv-fyn': 11615,
        'lorry': 11616,
        'tv2-bornholm': 11617,
        'tv3-sport-2-hd': 12034,
        'bbc-brit': 12396,
        'tv5-monde-europe': 12697,
        'national-geographic-people': 15032,
        'comedy-central': 15129,
        'cs-go': 2147483566,
        'zulu-comedy': 2147483567,
        'oiii': 2147483568,
        'discovery-science': 117,
    }

    program_dict = {}

    allChannelsChosen = False

    if user_channels[0] == 'all':
        allChannelsChosen = True

    if not allChannelsChosen:
        for user_channel in user_channels:
            user_channel = user_channel.lower()

            # Check if channel is in channel_indix dict, if not add channel as key
            if user_channel not in program_dict.keys():
                program_dict.update({user_channel: []})

            # Get index from dict
            index = channel_index[user_channel]

            for channel in channel_list:
                if channel['id'] == str(index):
                    program_dict[user_channel].append(channel['programs'])
    else:
        for channel in channel_index.keys():
            # Check if channel is in channel_indix dict, if not add channel as key
            if channel not in program_dict.keys():
                program_dict.update({channel: []})

            # Get index from dict
            index = channel_index[channel]

            for channel_test in channel_list:
                if channel_test['id'] == str(index):
                    program_dict[channel].append(channel_test['programs'])

    return program_dict


def convert_unix_time(unix_time: int, toShow: bool):
    """Convert UNIX times to hour and minutes to an int, e.g.: 1604692800 -> 2000\n
       Times are shifted from UTC to UTC+1 (CET)"""
    
    # TODO: Use datetime timezone to convert to my timezone

    time = datetime.utcfromtimestamp(unix_time)
    time += timedelta(hours=1)
    
    if toShow:
        time = time.strftime('%H:%M')
    else:
        time = int(time.strftime('%H%M'))

    return time


def print_all_programs(program_dict: dict):
    """Print all the programs in the provided dict"""
    for channel in program_dict.keys():
        # print channel name
        print(f'\n{channel.upper().replace("-", " ")}')
        for program_list in program_dict[channel]:
            for program in program_list:
                timeStart = int(program['start'])
                timeStart = convert_unix_time(timeStart, toShow=True)
                progsTitle = program['title']
                print(f"{timeStart} > {progsTitle}")
    print()


def print_time_program(program_dict: dict, timeStarts: list):
    """Find and print the program at the specified time on the channels defined in program_dict"""
    # Contains the program(s) that start at the specified time
    progsTime = {}

    # Check if channel is in progsTime dict, if not add channel as key
    for channel in program_dict.keys():
        if channel not in progsTime.keys():
            progsTime.update({channel: []})

    for channel in program_dict.keys():
        for program_list in program_dict[channel]:
            for program in program_list:
                for time in timeStarts:
                    # Get time start end end of program in UNIX time from HTML
                    time_data_unix_start = int(program['start'])
                    time_data_unix_end = int(program['stop'])

                    time_start = convert_unix_time(time_data_unix_start, toShow=False)
                    time_end = convert_unix_time(time_data_unix_end, toShow=False)

                    # Append the program that start at the specified time to dict progsTime
                    if time_start == int(time.replace(':', '')):
                        progsTime[channel].append(program)
                    # Append the program that is running at the specified time to dict progsTime
                    elif time_start < int(time.replace(':', '')) and time_end > int(time.replace(':', '')):
                        progsTime[channel].append(program)

    for channel in progsTime.keys():
        if len(progsTime[channel]) > 0:
            print(f'\n{channel.upper().replace("-", " ")}')
            for program in progsTime[channel]:
                progsTitle = program['title']
                timeStart_unix = int(program['start'])
                timeEnd_unix = int(program['stop'])
                # Times are shifted from UTC to UTC+1 (CET)
                time_start = convert_unix_time(timeStart_unix, toShow=True)
                time_end = convert_unix_time(timeEnd_unix, toShow=True)

                print(f'{time_start} - {time_end} > {progsTitle}')
        else:
            print(f'{channel.upper().replace("-", " ")}')
            print(f'There is no programs that start at this time: {", ".join(timeStarts)}\n')
    print()


def main(args):
    if not args.channel:
        print('No channels chosen: using default channels (dr1, tv2)')
        args.channel = ['dr1', 'tv2']

    if not args.time and not args.all:
        print('No time specified: using default time (20:00)')
        args.time = ['20:00']

    channel_list = get_channels()
    program_dict = get_programs(channel_list, args.channel)

    if args.time:
        print_time_program(program_dict, args.time)

    if args.all:
        print_all_programs(program_dict)


if __name__ == "__main__":
    args = argparse_setup()
    try:
        main(args)
    except KeyError:
        print('Check channel name or this scraper can\'t use one of the chosen channels')