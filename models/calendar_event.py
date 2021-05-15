from datetime import datetime

class CalendarEvent:

    @staticmethod
    def set_duration(start, end):
        difference = end - start
        return difference.total_seconds()

    def __init__(self, start: datetime, end: datetime, summary: str, description: str, raw_event=None):
        self.start = start
        self.end = end
        self.date = start.date()
        self.summary = summary
        self.description = description
        self.raw_event = raw_event
        self.duration_in_seconds = self.set_duration(start, end)
        self.duration_in_minutes = self.duration_in_seconds / 60.0
        self.duration_in_hours = self.duration_in_seconds / 3600.0
