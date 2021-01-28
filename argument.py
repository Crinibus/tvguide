from argparse import ArgumentParser


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
        '--justify-length',
        dest='justify_length',
        help='change justify length',
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
