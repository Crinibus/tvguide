import argparse

def validate_date_argument(arg):
    """Method to check argument --day for min and max value"""
    MIN_VAL = -1
    MAX_VAL = 6
    
    try:
        num = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError('Day argument must be a integer')

    if num < MIN_VAL or num > MAX_VAL:
        raise argparse.ArgumentTypeError(f'Day argument must be > {MIN_VAL} and < {MAX_VAL}')
    return num