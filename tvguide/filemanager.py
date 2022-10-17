import pathlib

class Filemanager:
    # root path of this repository
    root_path = pathlib.Path(__file__).parent.parent.absolute()
    defaults_ini_path = f"{root_path}/tvguide/defaults.ini"
