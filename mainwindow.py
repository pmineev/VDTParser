import wx
from wx import Frame, Panel, TextCtrl, BoxSizer, StaticText, Button, Size
from wx.adv import DatePickerCtrl
from datetime import date

from scrapers import get_leaderboards
from calc import get_deltas

from plotcanvas import PlotCanvas

import datetime

deltas = {'dates': [datetime.date(2021, 9, 8),
                    datetime.date(2021, 9, 9),
                    datetime.date(2021, 9, 13),
                    datetime.date(2021, 9, 16),
                    datetime.date(2021, 9, 17),
                    datetime.date(2021, 9, 19)],
          'abs_vdt': [10.26,
                      8.322,
                      11.613,
                      11.586,
                      13.541,
                      9.928],
          'abs_world': [10.260000000000002,
                        8.322000000000001,
                        15.979,
                        11.586,
                        13.621000000000002,
                        9.928],
          'rel_vdt': [55.1672222819658, 52.435259277928296,
                      59.132338713783795,
                      78.15704263356719, 75.77504196978175,
                      52.82818070558187],
          'rel_world': [55.16722228196581,
                        52.4352592779283,
                        104.62253650232437,
                        78.15704263356719,
                        76.56548622821812,
                        52.82818070558187]}
deltas2 = {'dates': [datetime.date(2021, 9, 1), datetime.date(2021, 9, 2), datetime.date(2021, 9, 3),
                     datetime.date(2021, 9, 6), datetime.date(2021, 9, 8), datetime.date(2021, 9, 9),
                     datetime.date(2021, 9, 10), datetime.date(2021, 9, 12), datetime.date(2021, 9, 13),
                     datetime.date(2021, 9, 14), datetime.date(2021, 9, 15), datetime.date(2021, 9, 16),
                     datetime.date(2021, 9, 17), datetime.date(2021, 9, 18), datetime.date(2021, 9, 19),
                     datetime.date(2021, 9, 20)],
           'abs_vdt': [7.024, 7.302, 7.831, 6.805, 6.375, 5.981, 5.994, 5.577, 3.04, 6.006, 7.424, 5.789, 7.744, 9.094,
                       4.945, 4.381],
           'abs_world': [7.024000000000001, 7.302000000000003, 7.8309999999999995, 6.805, 6.375, 5.981,
                         5.9940000000000015, 5.577000000000002, 7.405999999999999, 6.006, 9.677000000000001, 5.789,
                         7.824000000000002, 9.094000000000001, 4.945, 4.381000000000002],
           'rel_vdt': [40.863342835534354, 41.378137927126424, 43.52006224296988, 40.72411729503291, 34.27787934186472,
                       37.685086005922756, 42.88167119759622, 31.060985797827907, 15.47940322827028, 48.40815668574192,
                       41.0892185078592, 39.051538046411224, 43.33519865696698, 51.3640214628636, 26.312988878837867,
                       32.982007076714595],
           'rel_world': [40.86334283553436, 41.378137927126446, 43.52006224296988, 40.72411729503291, 34.27787934186472,
                         37.685086005922756, 42.88167119759623, 31.060985797827918, 48.490800759510236,
                         48.40815668574192, 61.18874486247235, 39.051538046411224, 43.9797639123103, 51.364021462863604,
                         26.312988878837867, 32.982007076714616]}

tick = True


class MainWindow(Frame):

    def __init__(self, parent=None, title='VDTParser'):
        Frame.__init__(self, parent, title=title)

        self.nickname = ''
        self.date_from = date.today()
        self.date_to = date.today()

        self.plot_canvas = None

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

    def OnNicknameChanged(self, e):
        self.nickname = e.GetEventObject().GetValue()
        print(self.nickname)

    def OnDateFromChanged(self, e):
        d = e.GetEventObject().GetValue()
        self.date_from = date(d.year, d.month + 1, d.day)

    def OnDateToChanged(self, e):
        d = e.GetEventObject().GetValue()
        self.date_to = date(d.year, d.month + 1, d.day)

    def OnStartButtonPressed(self, e):
        # leaderboards = get_leaderboards(self.date_from, self.date_to)
        # deltas = get_deltas(leaderboards, self.nickname)

        global tick
        if tick:
            self.plot_canvas.plot_deltas(deltas)
            tick = not tick
        else:
            self.plot_canvas.plot_deltas(deltas2)
            tick = not tick

        # self.plot_canvas.plot(0, deltas['dates'], deltas['rel_vdt'])
        # self.plot_canvas.plot(0, deltas['dates'], deltas['rel_world'])
        # self.plot_canvas.plot(1, deltas['dates'], deltas['abs_vdt'])
        # self.plot_canvas.plot(1, deltas['dates'], deltas['abs_world'])

    def OnExportButtonPressed(self, e):
        pass
