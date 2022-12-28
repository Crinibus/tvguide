import tvguide as tv


def main():
    args = tv.argparse_setup()

    tvguide = tv.TvGuide()

    tvguide.parse_arguments(args)

    api_data = tv.ApiManager.get_data(tvguide.relative_date)

    tvguide.parse_api_data(api_data)

    tvguide.print_programs()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by user")
