import wx
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class PlotCanvas(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent, -1)

        self.figure = Figure(tight_layout=True)

        self.axes = (self.figure.add_subplot(211),
                     self.figure.add_subplot(212))
        self.axes[0].set_xticks([])

        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, flag=wx.EXPAND)
        self.SetSizer(self.sizer)

    def plot_deltas(self, deltas):
        self.axes[0].clear()
        self.axes[1].clear()

        self.axes[0].set_title('Проценты всоса')
        self.axes[1].set_title('Абсолютные всосы')

        self.axes[0].plot(deltas['dates'], deltas['rel_vdt'])
        self.axes[0].plot(deltas['dates'], deltas['rel_world'])
        self.axes[1].plot(deltas['dates'], deltas['abs_vdt'])
        self.axes[1].plot(deltas['dates'], deltas['abs_world'])

        self.axes[0].set_yticks(deltas['rel_vdt'] + deltas['rel_world'], minor=True)
        self.axes[1].set_yticks(deltas['abs_vdt'] + deltas['abs_world'], minor=True)

        self.axes[0].set_xticks(deltas['dates'])
        self.axes[1].set_xticks(deltas['dates'])
        self.axes[1].xaxis.set_major_formatter(DateFormatter('%d.%m.%Y'))

        self.axes[0].grid(axis='x')
        self.axes[0].grid(axis='y', which='minor')
        self.axes[1].grid(axis='x')
        self.axes[1].grid(axis='y', which='minor')

        self.axes[0].legend(('VDT', 'По миру'))

        self.figure.autofmt_xdate(rotation=45)
        self.canvas.draw()
