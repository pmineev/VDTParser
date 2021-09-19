import wx
from wx import Frame, Panel, TextCtrl, BoxSizer, FlexGridSizer, GridSizer, StaticText, Button, Size
from wx.adv import DatePickerCtrl
from wxmplot import PlotPanel
from datetime import date


class Window(Frame):

    def __init__(self, parent=None, title='VDTParser'):
        Frame.__init__(self, parent, title=title)

        self.nickname = None
        self.date_from = None
        self.date_to = None

        self.plot_rel = None
        self.plot_abs = None

        self.init()
        self.SetMinSize(Size(800, 600))
        self.Show()

    def init(self):
        panel = Panel(self)

        hbox = FlexGridSizer(1, 4, 0, 0)

        controls_box = BoxSizer(wx.VERTICAL)

        nickname_control = TextCtrl(panel)
        nickname_control.SetHint('Введите никнейм')
        nickname_control.Bind(wx.EVT_TEXT, self.OnNicknameChanged)
        controls_box.Add(nickname_control, flag=wx.ALL | wx.EXPAND, border=10)

        dates_box = BoxSizer(wx.HORIZONTAL)
        from_text = StaticText(panel, label='от:')
        date_from_control = DatePickerCtrl(panel)
        date_from_control.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateFromChanged)
        to_text = StaticText(panel, label='до:')
        date_to_control = DatePickerCtrl(panel)
        date_to_control.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateToChanged)
        dates_box.Add(from_text, flag=wx.ALIGN_CENTER)
        dates_box.Add(date_from_control, flag=wx.LEFT | wx.RIGHT, border=10)
        dates_box.Add(to_text, flag=wx.ALIGN_CENTER)
        dates_box.Add(date_to_control, flag=wx.LEFT, border=10)
        controls_box.Add(dates_box, flag=wx.ALL, border=10)

        start_button = Button(panel, label='вперед!!!')
        start_button.Bind(wx.EVT_BUTTON, self.OnStartButtonPressed)
        controls_box.Add(start_button, flag=wx.ALL | wx.EXPAND, border=10)
        start_button.Bind(wx.EVT_BUTTON, self.OnExportButtonPressed)
        export_button = Button(panel, label='экспорт в xls')
        controls_box.Add(export_button, flag=wx.ALL | wx.EXPAND, border=10)

        hbox.Add(controls_box)

        plots_box = GridSizer(1, 0, 0)

        rel_plot = PlotPanel(panel, show_config_popup=False, size=(1000, 1000))
        plots_box.Add(rel_plot, flag=wx.EXPAND, proportion=1)

        abs_plot = PlotPanel(panel, show_config_popup=False, size=(1000, 1000))
        plots_box.Add(abs_plot, flag=wx.EXPAND, proportion=1)

        hbox.Add(plots_box, flag=wx.EXPAND)

        hbox.AddGrowableCol(1)

        panel.SetSizer(hbox)

    def OnNicknameChanged(self, e):
        self.nickname = e.GetEventObject().GetValue()
        print(self.nickname)

    def OnDateFromChanged(self, e):
        d = e.GetEventObject().GetValue()
        self.date_from = date(d.year, d.month+1, d.day)

    def OnDateToChanged(self, e):
        d = e.GetEventObject().GetValue()
        self.date_to = date(d.year, d.month+1, d.day)

    def OnStartButtonPressed(self, e):
        pass

    def OnExportButtonPressed(self, e):
        pass
