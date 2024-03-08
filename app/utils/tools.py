import datetime


def get_end_of_day(date: str) -> datetime.datetime:
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    end_of_day = date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)
    formatted_date = end_of_day.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return formatted_date


def get_start_of_day(date: str) -> datetime.datetime:
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    formatted_date = start_of_day.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return formatted_date


def parse_iso_datetime(date_str):
    """Parse an ISO 8601 datetime.datetime string to a datetime.datetime object."""
    if date_str.endswith("Z"):
        date_str = date_str[:-1] + "+00:00"
    return datetime.datetime.fromisoformat(date_str)


def format_dates_for_api(start_date, end_date):
    raw_start_date = start_date
    start_date = get_start_of_day(raw_start_date)
    raw_end_date = end_date
    if not raw_end_date:
        end_date = datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        end_date = get_end_of_day(end_date)
    return start_date, end_date
