#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Lottery generator GUI interface using wxPython
"""
import wx
import wx.adv
from wx.lib import intctrl

from common import OptionsData
import constants as C


class MainFrame(wx.Frame):
    """Main window of lottery generator
    """

    ID_MENU_ABOUT: wx.WindowIDRef = wx.NewIdRef()
    ID_MENU_EXIT: wx.WindowIDRef = wx.NewIdRef()
    ID_LOTTERY_TYPE: wx.WindowIDRef = wx.NewIdRef()

    options_data = OptionsData

    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=u"Lottery Numbers Generator",
            pos=wx.DefaultPosition,
            size=wx.Size(420, 245),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )
        self.SetFont(
            wx.Font(
                pointSize=C.FONT_POINT_SIZE,
                family=wx.FONTFAMILY_DEFAULT,
                style=wx.FONTSTYLE_NORMAL,
                weight=wx.FONTWEIGHT_NORMAL,
                underline=False,
                faceName=C.FONT_FACE,
            )
        )

        self.SetSizeHints(wx.DefaultSize)
        self.make_menu_bar()
        self.make_main_controls()
        self.make_status_bar()
        self.Layout()
        self.Fit()
        self.Centre(direction=wx.BOTH)

    def __del__(self):
        pass

    def make_menu_bar(self):
        """Create a menu bar on the frame
        """
        main_menu_bar = wx.MenuBar(style=0)

        file_menu = wx.Menu()

        exit_menu_item = wx.MenuItem(
            parentMenu=file_menu,
            id=self.ID_MENU_EXIT,
            text=u"E&xit",
            helpString=wx.EmptyString,
            kind=wx.ITEM_NORMAL,
        )
        file_menu.Append(menuItem=exit_menu_item)
        main_menu_bar.Append(menu=file_menu, title=u"&File")

        help_menu = wx.Menu()
        about_menu_item = wx.MenuItem(
            parentMenu=help_menu,
            id=self.ID_MENU_ABOUT,
            text=u"&About",
            helpString=wx.EmptyString,
            kind=wx.ITEM_NORMAL,
        )
        help_menu.Append(menuItem=about_menu_item)
        main_menu_bar.Append(menu=help_menu, title=u"&Help")

        self.SetMenuBar(menuBar=main_menu_bar)

        self.Bind(event=wx.EVT_MENU, handler=self.on_exit, source=exit_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_about, source=about_menu_item)

    def make_main_controls(self):
        """Create the controls on the frame
        """
        opt = self.options_data
        grid = wx.GridBagSizer(vgap=0, hgap=0)
        grid.SetFlexibleDirection(direction=wx.BOTH)
        grid.SetNonFlexibleGrowMode(mode=wx.FLEX_GROWMODE_SPECIFIED)

        choice_text = wx.StaticText(
            self,
            id=wx.ID_ANY,
            label=u"Choose type of lottery: ",
            pos=wx.Point(x=-1, y=-1),
            size=wx.DefaultSize,
            style=0,
        )
        choice_text.Wrap(width=-1)

        grid.Add(
            choice_text,
            pos=wx.GBPosition(row=1, col=1),
            span=wx.GBSpan(rowspan=1, colspan=1),
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
            border=5,
        )

        lottery_combo = wx.ComboBox(
            self,
            id=self.ID_LOTTERY_TYPE,
            value=C.LOTTERY_CHOICES[opt.lottery_type],
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            choices=C.LOTTERY_CHOICES,
            style=wx.CB_READONLY,
        )

        grid.Add(
            lottery_combo,
            pos=wx.GBPosition(row=1, col=2),
            span=wx.GBSpan(rowspan=1, colspan=1),
            flag=wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_VERTICAL,
            border=5,
        )

        lines_text = wx.StaticText(
            self,
            id=wx.ID_ANY,
            label=u"Lines: ",
            pos=wx.Point(x=-1, y=-1),
            size=wx.DefaultSize,
            style=0,
        )
        lines_text.Wrap(width=-1)
        grid.Add(
            lines_text,
            pos=wx.GBPosition(row=2, col=1),
            span=wx.GBSpan(rowspan=1, colspan=1),
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
            border=5,
        )

        lines_control = intctrl.IntCtrl(
            parent=self,
            value=opt.number_of_lines,
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=0,
            validator=wx.DefaultValidator,
            min=1,
            max=99,
            limited=True,
            allow_none=False,
            allow_long=False,
        )
        lines_control.SetMaxLength(len=2)
        lines_control.SetMaxSize(size=wx.Size(30, -1))
        grid.Add(
            lines_control,
            pos=wx.GBPosition(row=2, col=2),
            span=wx.GBSpan(rowspan=1, colspan=1),
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
            border=5,
        )

        radio_box = wx.RadioBox(
            self,
            id=wx.ID_ANY,
            label=u"Options",
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            choices=C.OPTIONS_CHOICES,
            majorDimension=1,
            style=wx.RA_SPECIFY_ROWS | wx.BORDER_RAISED,
        )
        radio_box.SetSelection(n=opt.option)
        flags = wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(
            radio_box,
            pos=wx.GBPosition(row=3, col=1),
            span=wx.GBSpan(rowspan=1, colspan=2),
            flag=flags,
            border=5,
        )

        button_sizer = wx.StdDialogButtonSizer()
        ok_button = wx.Button(parent=self, id=wx.ID_OK)
        button_sizer.AddButton(button=ok_button)
        cancel_button = wx.Button(parent=self, id=wx.ID_CANCEL)
        button_sizer.AddButton(button=cancel_button)
        button_sizer.Realize()
        grid.Add(
            button_sizer,
            pos=wx.GBPosition(row=5, col=1),
            span=wx.GBSpan(rowspan=1, colspan=2),
            flag=wx.ALIGN_CENTER_HORIZONTAL,
            border=5,
        )

        self.SetSizer(grid)
        lottery_combo.Bind(
            event=wx.EVT_COMBOBOX, handler=self.on_type_combo, id=self.ID_LOTTERY_TYPE
        )
        self.Bind(
            event=intctrl.EVT_INT, handler=self.on_line_control, source=lines_control
        )
        radio_box.Bind(event=wx.EVT_RADIOBOX, handler=self.on_radiobox)
        self.Bind(
            event=wx.EVT_BUTTON, handler=self.on_ok, source=ok_button, id=wx.ID_OK
        )
        self.Bind(
            event=wx.EVT_BUTTON,
            handler=self.on_cancel,
            source=cancel_button,
            id=wx.ID_CANCEL,
        )

    def make_status_bar(self):
        """Make the statusbar
        """
        __style__: str = wx.STB_DEFAULT_STYLE | wx.STB_SIZEGRIP | wx.ALWAYS_SHOW_SB
        main_status_bar = self.CreateStatusBar(
            number=1, style=__style__, id=wx.ID_ANY, name=wx.StatusBarNameStr
        )
        self.SetStatusBar(statusBar=main_status_bar)

    def on_exit(self, event):
        """Perform actions when user generates an exit event

        :param event:
        :return:
        """
        event.Skip()

    def on_about(self, event):
        """Perform actions when user requests an about box

        :param event:
        :return:
        """
        event.Skip()

    def on_type_combo(self, event):
        """Perform actions when user changes the combobox selection

        :param event:
        :return:
        """
        event.Skip()

    def on_line_control(self, event):
        """Perform actions when user changes the number in the line control

        :param event:
        :return:
        """
        event.Skip()

    def on_radiobox(self, event):
        """Perform actions when user chooses an option to action

        :param event:
        :return:
        """
        event.Skip()

    def on_cancel(self, event):
        """Perform actions when user presses the Cancel button

        :param event:
        :return:
        """
        event.Skip()

    def on_ok(self, event):
        """Perform actions when user presses the OK button

        :param event:
        :return:
        """
        event.Skip()
