import datetime
import uuid


def schedule_from_string(starts_at: datetime, schedule: str):
    date = dates(starts_at)
    events = [
        event
        for event in [to_slot(next(date), slot.upper()) for slot in schedule]
        if event is not None
    ]
    return (
        f"BEGIN:VCALENDAR\r\n"
        f"VERSION:2.0\r\n"
        f"PRODID:WORKCAL\r\n"
        f'{"".join(events)}'
        f"END:VCALENDAR\r\n"
    )


def to_slot(starts_at: datetime, slot: str):
    if slot == "M":
        start = starts_at.replace(hour=8, minute=0, second=0)
        return calendar_event("Morning", start, start.replace(hour=16))
    elif slot == "T":
        start = starts_at.replace(hour=16, minute=0, second=0)
        return calendar_event("Afternoon", start, start.replace(hour=23))
    elif slot == "N":
        start = starts_at - datetime.timedelta(days=1)
        start = start.replace(hour=22, minute=30)
        end = starts_at.replace(hour=8, minute=30, second=0)
        return calendar_event("Night", start, end)
    else:
        return None


def dates(start_date: datetime):
    start = start_date
    while True:
        yield start
        start = start + datetime.timedelta(days=1)


def calendar_event(name: str, start: datetime, end: datetime):
    return (
        f"BEGIN:VEVENT\r\n"
        f"UID:{uuid.uuid4().hex}\r\n"
        f"SUMMARY:{name}\r\n"
        f"DESCRIPTION:{name}\r\n"
        f"DTSTAMP:{calendar_timestamp(start)}\r\n"
        f"DTSTART:{calendar_timestamp(start)}\r\n"
        f"DTEND:{calendar_timestamp(end)}\r\n"
        f"END:VEVENT\r\n"
    )


def calendar_timestamp(date: datetime):
    return date.strftime("%Y%m%dT%H%M%S")
