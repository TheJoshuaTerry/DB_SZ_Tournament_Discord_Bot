from datetime import datetime, timedelta
import pytz


def convert_start_time(timestamp):
    # Parse the input string into a datetime object
    dt = datetime.fromisoformat(timestamp)

    # Convert to desired format: Month, Day, Year, and time
    formatted_date = dt.strftime("%B %d, %Y @ %I:%M %p")

    return formatted_date

def get_checkin_time(timestamp_str, minutes):
    # Parse the input string into a datetime object
    dt = datetime.strptime(timestamp_str, "%B %d, %Y @ %I:%M %p")

    # Subtract the specified number of minutes
    new_dt = dt - timedelta(minutes=minutes)

    # Convert to desired format: Month, Day, Year, and time
    formatted_date = new_dt.strftime("%B %d, %Y, %I:%M %p")

    return formatted_date
