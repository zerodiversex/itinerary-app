from core.models import Stop, Trip, StopTime, Connection, FootPath
from core.outils import seconds_to_hhmmss

def get_trip_ids_for_stop(stop_id: str, departure_time: int):
    potential_trips = Trip.objects.filter(departure_time_gta=departure_time, stop_id=stop_id).values_list('trip_id')
    return potential_trips

def raptor(start_station, end_station, departure_time=None, arrival_time=None):
    potential_trips = get_trip_ids_for_stop(None, departure_time)
    return None