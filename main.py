from pprint import pp
from datetime import date

from scrapers import get_leaderboards
from calc import filter_leaderboards, get_abs_vdt_deltas, get_abs_world_deltas, get_rel_vdt_deltas, get_rel_world_deltas
from mainwindow import Window

import wx


def main():
    date_from = date(2021, 9, 5)
    date_to = date(2021, 9, 17)
    nickname = 'Ccbbr'

    leaderboards = get_leaderboards(date_from, date_to)

    filtered_leaderboards = filter_leaderboards(leaderboards, nickname)
    abs_vdt_deltas = get_abs_vdt_deltas(filtered_leaderboards, nickname)
    abs_world_deltas = get_abs_world_deltas(filtered_leaderboards, nickname)
    rel_vdt_deltas = get_rel_vdt_deltas(filtered_leaderboards, nickname)
    rel_world_deltas = get_rel_world_deltas(filtered_leaderboards, nickname)

    pp(abs_vdt_deltas)
    pp(abs_world_deltas)
    pp(rel_vdt_deltas)
    pp(rel_world_deltas)


if __name__ == '__main__':
    # main()
    app = wx.App()
    wnd = Window()
    app.MainLoop()
