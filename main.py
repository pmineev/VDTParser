import wx

from mainwindow import MainWindow


def main():
    app = wx.App()
    MainWindow()
    app.MainLoop()


if __name__ == '__main__':
    main()
