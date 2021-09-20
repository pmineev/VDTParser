import wx
from wx import Frame, Panel, TextCtrl, BoxSizer, FlexGridSizer, GridSizer, StaticText, Button, Size
from wx.adv import DatePickerCtrl
from wxmplot import PlotPanel
from datetime import date
import matplotlib.dates as mdates

from scrapers import get_leaderboards
from calc import get_deltas


class Window(Frame):

    def __init__(self, parent=None, title='VDTParser'):
        Frame.__init__(self, parent, title=title)

        self.nickname = ''
        self.date_from = date.today()
        self.date_to = date.today()

        self.rel_plot = None
        self.abs_plot = None

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
        export_button = Button(panel, label='экспорт в xls')
        export_button.Bind(wx.EVT_BUTTON, self.OnExportButtonPressed)
        controls_box.Add(export_button, flag=wx.ALL | wx.EXPAND, border=10)

        hbox.Add(controls_box)

        plots_box = GridSizer(1, 0, 0)

        rel_plot = PlotPanel(panel, show_config_popup=False, size=(1000, 1000))
        self.rel_plot = rel_plot
        plots_box.Add(rel_plot, flag=wx.EXPAND, proportion=1)

        abs_plot = PlotPanel(panel, show_config_popup=False, size=(1000, 1000))
        self.abs_plot = abs_plot
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
        leaderboards = get_leaderboards(self.date_from, self.date_to)
        deltas = get_deltas(leaderboards, self.nickname)

        self.rel_plot.plot(list(deltas['rel_vdt'].keys()), deltas['rel_vdt'].values(), labelfontsize=5, title='проценты всоса')
        self.rel_plot.oplot(list(deltas['rel_world'].keys()), deltas['rel_world'].values(), labelfontsize=5)
        self.abs_plot.plot(list(deltas['abs_vdt'].keys()), deltas['abs_vdt'].values(), labelfontsize=5, title='абсолютные всосы')
        self.abs_plot.oplot(list(deltas['abs_world'].keys()), deltas['abs_world'].values(), labelfontsize=5)

    def OnExportButtonPressed(self, e):
        pass
