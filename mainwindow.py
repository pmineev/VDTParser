import wx
from wx import Frame, Panel, TextCtrl, BoxSizer, StaticText, Button, Size
from wx.adv import DatePickerCtrl
from datetime import date

from scrapers import ScraperThread
from events import SCRAPING_COMPLETEG
from calc import get_deltas

from plotcanvas import PlotCanvas


class MainWindow(Frame):

    def __init__(self, parent=None, title='VDTParser'):
        Frame.__init__(self, parent, title=title)

        self.nickname = ''
        self.date_from = date.today()
        self.date_to = date.today()

        self.plot_canvas = None
        self.scraper = None

        self.init()
        self.SetMinSize(Size(900, 600))
        self.Show()

    def init(self):
        hbox = BoxSizer(wx.HORIZONTAL)

        panel = Panel(self)

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

        panel.SetSizer(controls_box)

        hbox.Add(panel, flag=wx.EXPAND)
        self.plot_canvas = PlotCanvas(self)
        hbox.Add(self.plot_canvas, proportion=1, flag=wx.EXPAND)

        self.SetSizerAndFit(hbox)

        self.Bind(SCRAPING_COMPLETEG, self.OnScrapingCompleted)

    def OnNicknameChanged(self, e):
        self.nickname = e.GetEventObject().GetValue()

    def OnDateFromChanged(self, e):
        d = e.GetEventObject().GetValue()
        self.date_from = date(d.year, d.month + 1, d.day)

    def OnDateToChanged(self, e):
        d = e.GetEventObject().GetValue()
        self.date_to = date(d.year, d.month + 1, d.day)

    def OnStartButtonPressed(self, _):
        self.scraper = ScraperThread(self, self.date_from, self.date_to)

    def OnScrapingCompleted(self, e):
        deltas = get_deltas(e.leaderboards, self.nickname)
        self.plot_canvas.plot_deltas(deltas)

    def OnExportButtonPressed(self, e):
        pass
