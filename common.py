#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Lottery generator common classes using wxPython
"""
import dataclasses
import constants as C


@dataclasses.dataclass
class OptionsData:
    """Options store
    """
    lottery_type: int = C.LOTTERY_DEFAULT
    number_of_lines: int = 2
    option: int = C.OPTIONS_DEFAULT

    def get_lottery_name(self):
        """Return a text of the type of lottery to generate numbers for

        :return: str the text of the selected lottery type
        """
        return C.LOTTERY_CHOICES[self.lottery_type]

    def get_option_name(self):
        """Return a text value of action to be performed

        :return: str the text of the action option
        """
        return C.OPTIONS_CHOICES[self.option]


@dataclasses.dataclass
class ResultsData:
    """Data to be passed to the results display frame
    """
    saved: bool = False
    # generated is True if generated or
    # False if retrieved from file
    generated: bool = True
    number_of_lines = 0
    stored_date: str = None
    lottery_type_name: str = ''
    data = []

    def get_data_line(self, line: int) -> str:
        """Get one item from data

        :param line: int index of the data to retrieve
        :return: str  a line of data results
        """
        if line and line < self.number_of_lines:
            return self.data[line]
        return ''

    def set_data_line(self, newdata: str) -> None:
        """Append data to a list

        :param newdata: str the data to save
        :return: None
        """
        if newdata is not None:
            self.data.append(newdata)
