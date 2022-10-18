from typing import List
from .const import CHANNEL_NUMBER_INDEX
from .format import Format, ConfigManager
import time


class Channel:
    def __init__(self, channel_info: dict, verbose: bool = False) -> None:
        self.verbose = verbose
        self.id: str = channel_info['id']
        self.name = CHANNEL_NUMBER_INDEX[self.id]
        self.programs: List[Program] = []
        self._parse_channel_info(channel_info)

    def _parse_channel_info(self, channel_info: dict) -> None:
        for program_dict in channel_info['programs']:
            program = Program(program_dict, self.verbose)
            self.programs.append(program)

    def print_all_programs(self) -> None:
        for program in self.programs:
            print(program.start_time_and_title)
        print()

    def print_searches(self, search_terms: List[str]) -> None:
        for program in self.programs:
            for search in search_terms:
                search = Format.user_search(search)
                if search in program.title.lower():
                    print(program.time_and_title)
                    break
        print()

    def print_categories(self, categories: List[str]) -> None:
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
        for program in self.programs:
            if program.is_running:
                print(program.time_and_title)
        print()

    def print_times(self, times: List[str]) -> None:
        for program in self.programs:
            for print_time in times:
                print_time = Format.user_time(print_time)
                if program.is_running_at(print_time):
                    print(program.time_and_title)
                    break
        print()

    def __iter__(self):
        return iter(self.programs)


class Program:
    def __init__(self, program_info: dict, verbose: bool = False):
        self.info = program_info
        self.verbose = verbose
        self._format_info()

    def _format_info(self):
        self.id: str = self.info['id']
        self.title: str = self.info['title']
        self.categories: List[str] = [category.lower() for category in self.info['categories']]
        self.time_start_unix: int = self.info['start']
        self.time_stop_unix: int = self.info['stop']
        self.time_start: int = Format.convert_unix_time(self.time_start_unix, toShow=False)
        self.time_stop: int = Format.program_time_stop(time_start=self.time_start, time_stop=Format.convert_unix_time(self.time_stop_unix, toShow=False))
        self.time_start_show: str = Format.convert_unix_time(self.time_start_unix, toShow=True)
        self.time_stop_show: str = Format.convert_unix_time(self.time_stop_unix, toShow=True)

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

        return self.time_start_unix <= time_now < self.time_stop_unix

    def is_running_at(self, time: str):
        if self.time_start <= time < self.time_stop:
            return True

        return False

    def __str__(self) -> str:
        return self.time_and_title

    def __repr__(self) -> str:
        return f"Program(program_info={self.info})"
