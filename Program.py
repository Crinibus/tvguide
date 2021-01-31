from format import Format, Config


class Program:
    def __init__(self, program_info: dict, verbose: bool = False):
        self.info = program_info
        self.verbose = verbose
        self.format_info()

    def format_info(self):
        self.time_start_unix = self.info['start']
        self.time_stop_unix = self.info['stop']
        self.time_start = Format.convert_unix_time(self.time_start_unix, toShow=False)
        self.time_stop = Format.program_time_stop(time_start=self.time_start, time_stop=Format.convert_unix_time(self.time_stop_unix, toShow=False))
        self.time_start_show = Format.convert_unix_time(self.time_start_unix, toShow=True)
        self.time_stop_show = Format.convert_unix_time(self.time_stop_unix, toShow=True)
        self.title = self.info['title']
        self.categories = [cat.lower() for cat in self.info['categories']]
        self.id = self.info['id']

    @property
    def time_and_title(self) -> str:
        if self.verbose:
            return self.time_and_title_and_category

        return f"{self.time_start_show} - {self.time_stop_show} > {self.title}"

    @property
    def start_time_and_title(self) -> str:
        if self.verbose:
            return self.start_time_and_title_and_category

        return f"{self.time_start_show} > {self.title}"

    @property
    def time_and_title_and_category(self) -> str:
        time_and_title = f"{self.time_start_show} - {self.time_stop_show} > {self.title}"
        justify_length = Config.get_justify_length()

        if len(time_and_title) > justify_length:
            time_and_title_cut = f"{time_and_title[:justify_length]}..."
        else:
            time_and_title_cut = time_and_title

        return f"{time_and_title_cut.ljust(justify_length + 5)} ({', '.join(self.categories)})"

    @property
    def start_time_and_title_and_category(self) -> str:
        time_and_title = f"{self.time_start_show} > {self.title}"
        justify_length = Config.get_justify_length()

        if len(time_and_title) > justify_length:
            time_and_title_cut = f"{time_and_title[:justify_length]}..."
        else:
            time_and_title_cut = time_and_title

        return f"{time_and_title_cut.ljust(justify_length + 5)} ({', '.join(self.categories)})"

    def is_running(self, time: int):
        if time == self.time_start or (time > self.time_start and time < self.time_stop):
            return True
        
        return False

    def __str__(self) -> str:
        return self.time_and_title

    def __repr__(self) -> str:
        return f"Program(program_info={self.info})"
