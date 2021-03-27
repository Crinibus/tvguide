import pathlib

class Filemanager:
    @staticmethod
    def get_root_path():
        """Return root path of this repository"""
        return pathlib.Path(__file__).parent.absolute()
