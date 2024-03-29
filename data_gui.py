#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Lottery generator numbers GUI interface using wxPython
"""

import wx
from common import ResultsData
import constants as C


class ResultsFrame(wx.Frame):
    """Data window of lottery generator
    """

    def __init__(self, parent, results) -> None:
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="Lottery Numbers",
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
        self.make_main_controls(results)
        self.Layout()
        self.Fit()
        self.Centre(direction=wx.BOTH)

    def __del__(self):
        pass

    def make_main_controls(self, results: ResultsData) -> None:
        """Create the controls on the frame

        :param results: the data to display
        :return:
        """

        def unwrap(some: str) -> str:
            """Remove characters "[". "]" and "'" from a string

            :param some: str the string to process
            :return:
            """
            return some.translate({ord(i): None for i in "[]'"})

        grid = wx.GridBagSizer(vgap=0, hgap=0)
        grid.SetFlexibleDirection(direction=wx.BOTH)
        grid.SetNonFlexibleGrowMode(mode=wx.FLEX_GROWMODE_SPECIFIED)
        action: str = "Generated " if results.generated else "Stored "
        label: str = action + results.lottery_type_name + " Lottery numbers: "
        choice_text = wx.StaticText(
            self,
            id=wx.ID_ANY,
            label=label,
            pos=wx.Point(x=-1, y=-1),
            size=wx.DefaultSize,
            style=0,
        )
        choice_text.Wrap(width=-1)
        flags: int = wx.ALIGN_CENTER_VERTICAL | wx.ALL
        span = wx.GBSpan(rowspan=1, colspan=1)
        border: int = 5
        grid.Add(
            choice_text,
            pos=wx.GBPosition(row=1, col=1),
            span=span,
            flag=flags | wx.ALIGN_CENTER_HORIZONTAL,
            border=border,
        )

        line: int = 0
        for line in range(results.get_data_length()):
            data_item = unwrap(results.get_data_item(line))
            text: str = f"Line {line + 1}: " + data_item
            control = wx.StaticText(
                self,
                id=wx.ID_ANY,
                label=text,
                pos=wx.Point(x=-1, y=-1),
                size=wx.DefaultSize,
                style=0,
            )
            grid.Add(
                control,
                pos=wx.GBPosition(row=line + 2, col=1),
                span=span,
                flag=flags,
                border=border,
            )

        info = wx.StaticText(
            self,
            id=wx.ID_ANY,
            label="",
            pos=wx.Point(x=-1, y=-1),
            size=wx.DefaultSize,
            style=0,
        )
        grid.Add(
            info,
            pos=wx.GBPosition(row=line + 3, col=1),
            span=span,
            flag=flags,
            border=border,
        )

        if results.is_retrieved():
            info.SetLabelText("Saved on " + results.stored_date)
        else:
            info.SetLabelText("")

        button_sizer = wx.StdDialogButtonSizer()
        ok_button = wx.Button(parent=self, id=wx.ID_OK)
        button_sizer.AddButton(button=ok_button)
        button_sizer.Realize()
        grid.Add(
            button_sizer,
            pos=wx.GBPosition(row=results.get_data_length() + 3, col=1),
            span=wx.GBSpan(rowspan=1, colspan=2),
            flag=wx.ALIGN_CENTER_HORIZONTAL,
            border=5,
        )
        self.SetSizer(grid)

        self.Bind(
            event=wx.EVT_BUTTON,
            handler=self.on_ok,
            source=ok_button,
            id=wx.ID_OK,
        )

    def on_ok(self, event) -> None:
        """Perform actions when OK button clicked

        :param event:
        :return: None
        """
        self.Close()
        event.Skip()
