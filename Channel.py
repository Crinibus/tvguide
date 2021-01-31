from datetime import datetime
from Program import Program
from const import CHANNEL_NUMBER_INDEX
from format import Format


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
        time = datetime.now()
        time_now = time.strftime('%H%M')

        print(f"\n{Format.channel_name(self.name)}:")
        for program in self.programs:
            if program.is_running(int(time_now)):
                print(program.time_and_title)
        print()

    def print_times(self, times: list) -> None:
        print(f"\n{Format.channel_name(self.name)}:")
        for program in self.programs:
            for time in times:
                time = Format.user_time(time)
                if program.is_running(time):
                    print(program.time_and_title)
                    break
        print()
