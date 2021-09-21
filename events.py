from wx.lib.newevent import NewEvent
from wx import PostEvent


ScrapingCompletedEvent, SCRAPING_COMPLETED = NewEvent()

ProgressTickEvent, PROGRESS_TICK = NewEvent()


class EventPoster:
    def __init__(self, destination, event):
        self.destination = destination
        self.event = event

    def post(self):
        PostEvent(self.destination, self.event)
