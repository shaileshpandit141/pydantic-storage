from datetime import datetime, timezone


def get_utc_time_now() -> datetime:
    return datetime.now(timezone.utc)
