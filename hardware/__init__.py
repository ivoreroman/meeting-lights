from datetime import datetime, timedelta
import math
from .seven_segment import SevenSegmentDisplay

def minutes_difference_from_now(date):
    """
    Returns an int with the minutes difference from now to the current date
    """
    now = datetime.now()
    return math.floor((date - now)/timedelta(minutes=1))

def date_to_seven_segments(date):
    """
    Sends the time differece from current date in minutes
    to the two seven segment displays
    """
    # Pin configuration: A B C D E F G
    # https://gpiozero.readthedocs.io/en/stable/_images/pin_layout.svg
    # Pins are the ones marked as GPIOXX
    minutes_left = SevenSegmentDisplay(27, 22, 5, 6, 13, 19, 26)
    minutes_right = SevenSegmentDisplay(23, 24, 25, 12, 16, 20, 21)

    # Get minutes difference
    minutes_difference = minutes_difference_from_now(date)
    minutes_difference = 99 if minutes_difference > 99 else minutes_difference

    # Convert int to a string array
    minutes_array = [str(digit) for digit in str(minutes_difference)]

    if minutes_difference < 10:
        minutes_left.display("0")
        minutes_right.display(minutes_array[0])
    else:
        minutes_left.display(minutes_array[-2])
        minutes_right.display(minutes_array[-1])
    return True
