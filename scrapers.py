from threading import Thread
from wx import PostEvent

from aiohttpclient import get_vdt_list, get_leaderboards_htmls
from parsers import parse_vdt_list, parse_flights
from events import ScrapingCompletedEvent, ProgressTickEvent, EventPoster


class ScraperThread(Thread):
    def __init__(self, notify_window, date_from, date_to):
        Thread.__init__(self)

        self.notify_window = notify_window
        self.date_from = date_from
        self.date_to = date_to

        self.start()

    def run(self):
        fetch_event_poster = EventPoster(self.notify_window, ProgressTickEvent(type='fetch'))

        vdt_list_html = get_vdt_list(fetch_event_poster)
        leaderboard_htmls = get_leaderboards_htmls(self.date_from, self.date_to, fetch_event_poster)

        leaderboards = parse_vdt_list(vdt_list_html, self.date_from, self.date_to)

        for leaderboard, html in zip(leaderboards, leaderboard_htmls):
            flights, world_record = parse_flights(html)
            leaderboard.flights = flights
            leaderboard.world_record = world_record

        PostEvent(self.notify_window, ScrapingCompletedEvent(leaderboards=leaderboards))
