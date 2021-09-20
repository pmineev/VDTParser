import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class PlotCanvas(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent, -1)

        self.figure = Figure()
        self.axes = (self.figure.add_subplot(211),
                     self.figure.add_subplot(212))

        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, flag=wx.EXPAND)
        self.SetSizer(self.sizer)

    def plot(self, index, *args, **kwargs):
        self.axes[index].plot(*args, **kwargs)
        self.canvas.draw()
