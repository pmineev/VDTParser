import wx

from mainwindow import Window


def main():
    app = wx.App()
    Window()
    app.MainLoop()


if __name__ == '__main__':
    main()
