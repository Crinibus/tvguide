from typing import Iterator, List
import time

from tvguide.const import CHANNEL_NUMBER_INDEX
from tvguide.format import Format
from tvguide.config import ConfigManager


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

    def is_running_at(self, time: int) -> bool:
        return self.time_start <= time < self.time_stop

    def __str__(self) -> str:
        return self.time_and_title

    def __repr__(self) -> str:
        return f"Program(program_info={self.info})"


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

    def print_searches(self, search_terms: List[str]) -> None:
        for search_term in search_terms:
            programs_with_search_term = self._get_programs_with_search_term(search_term)
            for program in programs_with_search_term:
                print(program.time_and_title)

    def print_categories(self, categories: List[str]) -> None:
        for category in categories:
            programs_with_category = self._get_programs_with_category(category)
            for program in programs_with_category:
                print(f"{program.time_and_title} ({category.capitalize()})")

    def print_currently_running(self) -> None:
        running_program = self._get_currently_running_program()

        if not running_program:
            print(
                "*Could not find a running program"
                " - if the time right now is after midnight before 6 am, try getting programs for yesterday*"
            )
            return

        print(running_program.time_and_title)

    def print_times(self, times: List[str]) -> None:
        for program in self._get_programs_with_show_times(times):
            print(program.time_and_title)

    def _get_currently_running_program(self) -> Program:
        for program in self.programs:
            if program.is_running:
                return program

    def _get_programs_with_category(self, category: str) -> List[Program]:
        programs_with_category: List[Program] = []
        for program in self.programs:
            if category.lower() in program.categories or program.categories == [] and category in ["nyheder"]:
                programs_with_category.append(program)
        return programs_with_category

    def _get_programs_with_search_term(self, search_term: str) -> List[Program]:
        programs_with_search_term: List[Program] = []
        for program in self.programs:
            if search_term.lower() in program.title.lower():
                programs_with_search_term.append(program)
        return programs_with_search_term

    def _get_programs_with_show_times(self, show_times: List[str]) -> Iterator[Program]:
        for program in self.programs:
            for show_time in show_times:
                time_int = Format.user_time(show_time)
                if program.is_running_at(time_int):
                    yield program

    def __iter__(self):
        return iter(self.programs)
