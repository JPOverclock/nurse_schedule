from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

from schedule import schedule_from_string
from datetime import datetime

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Schedule Generator</title>
    </head>
    <body>
        <h1>Schedule Generator</h1>
        <div>
        <form action="/generate_schedule" method="get">
            <label for="start_date">Start date:</label><br>
            <input type="date" id="start_date" name="start_date"><br>
            <label for="schedule">Schedule (sequence of M, T, N):</label><br>
            <input type="text" id="schedule" name="schedule">
            <input type="submit" value="Submit">
        </form>
        </div>
    </body>
    </html>
    """


@app.get("/generate_schedule")
async def generate_schedule(start_date: str, schedule: str):
    date = datetime.strptime(start_date, "%Y-%m-%d")
    calendar = schedule_from_string(date, schedule)
    response = Response(content=calendar, media_type="text/calendar; charset=utf-8")
    response.headers["Content-Disposition"] = f"inline; filename=calendar.ics"
    return response
