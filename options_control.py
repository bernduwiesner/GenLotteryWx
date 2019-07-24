#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Lottery generator using wxPython
"""

from pathlib import Path
from random import sample
import shelve
import time
import wx
import wx.adv
import constants as C
import options_gui
from common import OptionsData, ResultsData
from data_gui import ResultsFrame


class GenLotteryMainFrame(options_gui.MainFrame):
    """ A Controller sub class of MainFrame
    """
    options_data = OptionsData()
    # This is the save file path name with no extension
    _saved_file = C.SAVE_FILE_DIR + options_data.get_lottery_name()
    dataList = []

    def __init__(self, parent):
        options_gui.MainFrame.__init__(self, parent)
        self.update_status()

    def update_status(self, text=None) -> None:
        """Utility function used to update the status bar
        :param text: text to display
        :return: None
        """
        status_bar = self.GetStatusBar()
        if text is None:
            opt = self.options_data
            status_bar.SetStatusText(f"OPTIONS - Action: "
                                     f"{opt.get_option_name()}"
                                     f", Type: "
                                     f"{opt.get_lottery_name()}"
                                     f", Lines: "
                                     f"{opt.number_of_lines}")
        else:
            status_bar.SetStatusText(text)

    def on_exit(self, event):
        """Close the frame and terminate the application."""
        self.Close(force=True)
        event.Skip()

    def on_about(self, _):
        about_info = wx.adv.AboutDialogInfo()
        about_info.SetName(C.PROGRAM)
        about_info.SetVersion(C.VERSION)
        about_info.SetDescription(u"Lottery numbers generator with wxPython")
        about_info.SetCopyright(u"(C) 2019-")
        about_info.AddDeveloper(C.AUTHOR)

        wx.adv.AboutBox(about_info)

    def on_type_combo(self, event):
        opt = self.options_data
        opt.lottery_type = event.GetSelection()
        opt.lottery_type_name = C.LOTTERY_CHOICES[
            opt.lottery_type]
        self._saved_file = C.SAVE_FILE_DIR\
            + opt.lottery_type_name

        self.update_status()
        event.Skip()

    def on_line_control(self, event):
        opt = self.options_data
        opt.number_of_lines = event.GetValue()
        self.update_status()
        event.Skip()

    def on_radiobox(self, event):
        opt = self.options_data
        opt.option = event.GetSelection()
        opt.option_name = C.OPTIONS_CHOICES[opt.option]
        self.update_status()
        event.Skip()

    def on_cancel(self, event):
        self.on_exit(event)

    def on_ok(self, event):
        opt = self.options_data
        if opt.option == 3:
            self.delete_saved_file()
        elif opt.option == 2:
            self.show_saved()
        else:
            self.generate_numbers()
        event.Skip()

    def generate_numbers(self) -> None:
        """Generate several random numbers and optionally save them
        :return:
        """

        def add_leading_zero(values: []) -> []:
            """Add a leading zero to numbers in the list < 10
            :param values: list of numbers
            :return: array containing formatted numbers
            """
            return [f"{v:02d}" for v in values]

        def choose_numbers(maximum: int, quantity: int) -> []:
            """Generate the random numbers required
            :param maximum: the highest number to choose from
            :param quantity: the number of numbers to generate
            :return: a sorted list of generated numbers
            """
            valid_range: range = range(C.RULE_START, maximum)
            return add_leading_zero(sorted(sample(valid_range, quantity)))

        result = ResultsData
        length = len(result.data)
        del result.data[:length]

        opt = self.options_data
        result.lottery_type_name = opt.get_lottery_name()
        result.number_of_lines = opt.number_of_lines

        main_max, main_qty,\
            extra_max, extra_qty = C.RULES[opt.get_lottery_name()]

        shelf = None
        result.generated = True
        if opt.option == 1:
            msg = 'The generated numbers have not been saved'
            result.saved = False
            self.update_status(msg)
        else:
            result.saved = True
            directory = Path(C.SAVE_FILE_DIR)
            if not directory.exists():
                directory.mkdir(parents=True)
            shelf = shelve.open(filename=self._saved_file,
                                protocol=C.SHELF_PROTOCOL)
            shelf[C.SHELF_ARGS['DATE']] = time.time()
            shelf[C.SHELF_ARGS['TYPE']] =\
                C.LOTTERY_CHOICES[opt.lottery_type]
            shelf[C.SHELF_ARGS['LINES']] = opt.number_of_lines

        # count the actual number of lines generated
        count: int = 0
        # generate the required number of lines
        for _ in range(opt.number_of_lines):
            # x_1 holds the first group of numbers generated
            # main_max is the the highest number to generate plus 1
            # main_qty is the quantity of numbers to generate each line
            x_1: [] = choose_numbers(maximum=main_max, quantity=main_qty)

            # x_2 holds the secondary group of numbers generated if
            # any are required
            # extra_max is the the highest number to generate plus 1
            # extra_qty is the quantity of numbers to
            # generate in each line
            x_2: [] = None
            # only generate the second group of numbers if required
            # if extra_qty > 0
            if extra_qty:
                x_2 = choose_numbers(maximum=extra_max, quantity=extra_qty)
            # If shelf is None it means no_save was specified
            if shelf is not None:
                shelf[C.SHELF_ARGS['PART1'] + str(count)] = x_1
                # Save the extra numbers even if there are none to save
                # will return None on subsequent reading
                shelf[C.SHELF_ARGS['PART2'] + str(count)] = x_2
            count += 1
            result.data.append(str(x_1) + ' - ' + str(x_2))
        # close the save file if there is one
        if opt.get_option_name() != C.OPTIONS_CHOICES[1]:
            shelf.close()
        test = opt.get_option_name() == C.OPTIONS_CHOICES[1]
        msg = f"The numbers have{' not' if test else ''}" \
            f" been saved and {count} lines were generated"
        self.update_status(msg)
        frm = ResultsFrame(None, result)
        frm.Show()

    def delete_saved_file(self) -> None:
        """Delete a previously saved file
        :return: None
        """
        # add the filename extension
        file_name = self._saved_file + C.SAVE_FILE_TYPE
        path = Path(file_name)
        file_exists = path.exists()
        if file_exists:
            path.unlink()
        msg = f"File: <{file_name}> was " \
            f"{'deleted' if file_exists else 'not found'}"
        self.update_status(msg)

    def show_saved(self) -> None:
        """Display a previously generated and saved batch of numbers
        :return: None
        """
        opt = self.options_data
        # add the filename extension
        path = Path(self._saved_file + C.SAVE_FILE_TYPE)
        if path.exists() and path.is_file():
            shelf = shelve.open(filename=self._saved_file,
                                flag=C.SHELF_READONLY,
                                protocol=C.SHELF_PROTOCOL)
            save_time = time.localtime(shelf[C.SHELF_ARGS['DATE']])
            result = ResultsData
            length = len(result.data)
            del result.data[:length]

            result.saved = False
            result.generated = False
            result.lottery_type_name = opt.get_lottery_name()
            result.stored_date = time.strftime(C.DATE_FORMAT, save_time)
            count = 0
            for line in range(shelf[C.SHELF_ARGS['LINES']]):
                # Don't display second group if none exist
                x_1 = shelf[C.SHELF_ARGS['PART1'] + str(line)]
                x_2 = shelf[C.SHELF_ARGS['PART2'] + str(line)] or ''
                result.data.append(str(x_1) + ' - ' + str(x_2))
                count += 1
            result.number_of_lines = count
            shelf.close()
            frm = ResultsFrame(None, result)
            frm.Show()
        else:
            msg = f"File <{path}> is missing"
            self.update_status(msg)