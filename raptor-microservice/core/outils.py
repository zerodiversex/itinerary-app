from datetime import datetime, timedelta
from core.models import Stop, Route, Trip, Transfer, StopTime, Connection, FootPath
from math import sin, cos, sqrt, asin, radians, ceil


class KeyList(object):
    # bisect doesn't accept a key function before 3.10,
    # so we build the key into our sequence.
    def __init__(self, l, key):
        self.l = l
        self.key = key
    def __len__(self):
        return len(self.l)
    def __getitem__(self, index):
        return self.key(self.l[index])

def time_to_seconds(input_time: str) -> int:
    """Converts a time string to seconds since midnight."""
    try:
        time = datetime.strptime(input_time, "%H:%M:%S")
        time_in_seconds = time.hour * 3600 + time.minute * 60 + time.second
        if time_in_seconds < 10800:
            time_in_seconds += 86400
    except:
        except_times = input_time.split(":")
        except_time = f"00:{except_times[1]}:{except_times[2]}"
        time = datetime.strptime(except_time, "%H:%M:%S")
        time_in_seconds = time.hour * 3600 + time.minute * 60 + time.second
        if time_in_seconds < 10800:
            time_in_seconds += 86400

    return time_in_seconds


def seconds_to_hhmmss(seconds: int) -> str:
    """Converts seconds since midnight to a time string."""
    if seconds > 86400:
        seconds -= 86400
    return str(timedelta(seconds=seconds))


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return ceil(n * multiplier) / multiplier


def haversine_distance(from_stop_lat, from_stop_lon, to_stop_lat, to_stop_lon):
    from_stop_lat, from_stop_lon, to_stop_lat, to_stop_lon = map(radians, [from_stop_lat, from_stop_lon, to_stop_lat, to_stop_lon])
    dlat = to_stop_lat - from_stop_lat
    dlon = to_stop_lon - from_stop_lon
    r = 6371  # radius of Earth in kilometers
    a = sin(dlat / 2) ** 2 + cos(from_stop_lat) * cos(to_stop_lat) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    speed = 2/3600
    distance = round_up(r * c, 2)

    return ceil(distance / speed)




