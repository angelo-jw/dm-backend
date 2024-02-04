from datetime import datetime


def get_end_of_day(date: str) -> datetime:
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    end_of_day = date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)
    formatted_date = end_of_day.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return formatted_date


def parse_iso_datetime(date_str):
    """Parse an ISO 8601 datetime string to a datetime object."""
    if date_str.endswith("Z"):
        date_str = date_str[:-1] + "+00:00"
    return datetime.fromisoformat(date_str)
