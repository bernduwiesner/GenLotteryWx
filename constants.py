#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Lottery generator using wxPython
"""
from pathlib import Path
import wx

VERSION = "0.0.1"
AUTHOR = "Bernd U. Wiesner"
PROGRAM = "Lottery Generator wx"

ID_MENU_ABOUT = wx.NewIdRef()
ID_MENU_EXIT = wx.NewIdRef()
ID_LOTTERY_TYPE = wx.NewIdRef()

LOTTERY_CHOICES = [
    "LOTTO",
    "EUROMILLIONS",
    "SETFORLIFE",
    "LOTTO-HOTPICKS",
    "EUROMILLIONS-HOTPICKS",
    "THUNDERBALL",
]
LOTTERY_DICT = {k: v for k, v in enumerate(LOTTERY_CHOICES)}
LOTTERY_DEFAULT = 1

OPTIONS_CHOICES = ["Save", "No Save", "Show", "Delete"]
OPTIONS_DICT = {k: v for k, v in enumerate(OPTIONS_CHOICES)}
OPTIONS_DEFAULT = 1

# Rules for each type of lottery
RULES: {str: [int, int, int, int]} = {
    # lottery_type: [main_max, main_qty, extra_max, extra_qty]
    LOTTERY_CHOICES[0]: [60, 6, False, False],
    LOTTERY_CHOICES[1]: [51, 5, 13, 2],
    LOTTERY_CHOICES[2]: [48, 5, 11, 1],
    LOTTERY_CHOICES[3]: [60, 5, False, False],
    LOTTERY_CHOICES[4]: [51, 5, False, False],
    LOTTERY_CHOICES[5]: [40, 5, 15, 1],
}

# The smallest number to generate
RULE_START: int = 1

# minimum number of lines to generate
MIN_LINES: int = 1
# maximum number of lines to generate.
# This is an arbitrary but reasonable limit
MAX_LINES: int = 99
# default number of lines to generate
DEFAULT_LINES: int = 2

# path to the saved files
# currently a sub directory of the user's home directory
SAVE_FILE_DIR: str = str(Path.home()) + "/lottery-db/"
# filename extension for saved files
SAVE_FILE_TYPE: str = ".db"

# a dictionary of shelf keys
SHELF_ARGS: {str, str} = {
    # dictionary key: shelf namespace key
    "DATE": "d",
    "TYPE": "t",
    "LINES": "l",
    "PART1": "x1",
    "PART2": "x2",
}
# protocol to use for saved file
SHELF_PROTOCOL: int = 4
# file mode when reading saved file
SHELF_READONLY: str = "r"

# date display format
DATE_FORMAT = "%A %d %B %Y at %X %Z"

FONT_POINT_SIZE = 14
FONT_FACE = "Helvetica"
