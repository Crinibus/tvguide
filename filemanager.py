import pathlib


def get_root_path_repo():
    """Return root path of this repository"""
    return pathlib.Path(__file__).parent.absolute()
