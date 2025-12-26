from __future__ import annotations
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Dublin")

def now() -> datetime:
    return datetime.now(TZ)

def to_iso(dt: datetime) -> str:
    return dt.isoformat()

def from_iso(s: str) -> datetime:
    return datetime.fromisoformat(s)

def parse_user_datetime(s: str) -> datetime | None:
    s = s.strip()
    try:
        dt = datetime.strptime(s, "%Y-%m-%d %H:%M")
        return dt.replace(tzinfo=TZ)
    except ValueError:
        return None

def minutes_from_now(minutes: int) -> datetime:
    return now() + timedelta(minutes=minutes)

def is_reached(iso_time: str) -> bool:
    return now() >= from_iso(iso_time)
