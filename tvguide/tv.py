from datetime import datetime
from .const import CHANNEL_NUMBER_INDEX
from .format import Format, ConfigManager
import time


class Channel:
    def __init__(self, channel_info: dict, verbose: bool = False) -> None:
        self.verbose = verbose
        self.id = channel_info['id']
        self.name = CHANNEL_NUMBER_INDEX[self.id]
        self.programs = []
        self.format_program_info(channel_info)

    def format_program_info(self, channel_info: dict) -> None:
        for program in channel_info['programs']:
            self.add_program(program)

    def add_program(self, program_info: dict) -> None:
        new_program = Program(program_info, self.verbose)
        self.programs.append(new_program)

    def print_all_programs(self) -> None:
        print(f"\n{Format.channel_name(self.name)}:")
        for program in self.programs:
            print(program.start_time_and_title)
        print()

    def print_searches(self, search_terms: list) -> None:
        print(f"\n{Format.channel_name(self.name)}:")
        for program in self.programs:
            for search in search_terms:
                search = Format.user_search(search)
                if search in program.title.lower():
                    print(program.time_and_title)
                    break
        print()

    def print_categories(self, categories: list) -> None:
        print(f"\n{Format.channel_name(self.name)}:")
        for program in self.programs:
            for category in categories:
                category = category.lower()
                if category in program.categories:
                    print(f"{program.time_and_title} ({category.capitalize()})")
                    break
                elif program.categories == [] and category in ['nyheder']:
                    print(f"{program.time_and_title} ({category.capitalize()})")
                    break
        print()

    def print_currently_running(self) -> None:
        print(f"\n{Format.channel_name(self.name)}:")
        for program in self.programs:
            if program.is_running:
                print(program.time_and_title)
        print()

    def print_times(self, times: list) -> None:
        print(f"\n{Format.channel_name(self.name)}:")
        for program in self.programs:
            for time in times:
                time = Format.user_time(time)
                if program.is_running_at(time):
                    print(program.time_and_title)
                    break
        print()

    def __iter__(self):
        return iter(self.programs)


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
        justify_length = ConfigManager.get_justify_length()

        if len(time_and_title) > justify_length:
            time_and_title_cut = f"{time_and_title[:justify_length]}..."
        else:
            time_and_title_cut = time_and_title

        return f"{time_and_title_cut.ljust(justify_length + 5)} ({', '.join(self.categories)})"

    @property
    def start_time_and_title_and_category(self) -> str:
        time_and_title = f"{self.time_start_show} > {self.title}"
        justify_length = ConfigManager.get_justify_length()

        if len(time_and_title) > justify_length:
            time_and_title_cut = f"{time_and_title[:justify_length]}..."
        else:
            time_and_title_cut = time_and_title

        return f"{time_and_title_cut.ljust(justify_length + 5)} ({', '.join(self.categories)})"

    @property
    def is_running(self) -> bool:
        time_now = time.time()

        if time_now == self.time_start_unix or (self.time_start_unix < time_now < self.time_stop_unix):
            return True

        return False

    def is_running_at(self, time: str):
        if self.time_start <= time < self.time_stop:
            return True

        return False

    def __str__(self) -> str:
        return self.time_and_title

    def __repr__(self) -> str:
        return f"Program(program_info={self.info})"
