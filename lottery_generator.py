#!/usr/bin/env python3
#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Lottery generator using wxPython
"""
import wx

from options_control import GenLotteryMainFrame


def main() -> None:
    """Application main

    :return: None
    """

    app = wx.App()
    frm = GenLotteryMainFrame(parent=None)
    frm.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
