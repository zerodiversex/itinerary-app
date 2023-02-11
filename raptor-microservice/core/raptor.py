from core.models import Stop, Trip, StopTime, Connection, FootPath
from core.outils import seconds_to_hhmmss


def raptor(start_station, end_station, departure_time=None, arrival_time=None):
    return None