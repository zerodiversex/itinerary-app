from route_search_engine.models import Stop, Trip, StopTime, Connection, FootPath
from route_search_engine.outils import seconds_to_hhmmss


def connection_scan(start_station, end_station, departure_time=None, arrival_time=None):
    stops = {stop[0]: float('inf') for stop in Stop.objects.all().values_list('stop_id')}
    trips = {trip[0]: None for trip in Trip.objects.all().values_list('trip_id')}
    journey = {stop[0]: (None, None, None) for stop in Stop.objects.all().values_list('stop_id')}

    stops[start_station] = departure_time

    for footpath in FootPath.objects.filter(transfer_dep_stop__stop_id=start_station):
        stops[footpath.transfer_arr_stop.stop_id] = departure_time + footpath.transfer_duration

    nbr_connection = 1
    for cdep_stop, cdep_time, carr_stop, carr_time, ctrip_id, cmode_transport, route in Connection.objects.filter(
            dep_time__gte=departure_time).order_by('dep_time').values_list('dep_stop__stop_id', 'dep_time', 'arr_stop__stop_id', 'arr_time', 'trip_id', 'mode_transport', 'route__route_short_name'):
        if cdep_time >= stops[end_station]:
            break
        if trips[ctrip_id] != None or stops[cdep_stop] <= cdep_time:
            if trips[ctrip_id] == None:
                trips[ctrip_id] = \
                (cdep_stop, cdep_time, carr_stop, carr_time, ctrip_id,
                cmode_transport, route)
            if carr_time < stops[carr_stop]:
                for transfer_dep_stop, transfer_arr_stop, transfer_duration in FootPath.objects.filter(
                        transfer_dep_stop__stop_id=carr_stop).values_list('transfer_dep_stop__stop_id',
                                                                          'transfer_arr_stop__stop_id',
                                                                          'transfer_duration'):
                    if carr_time + transfer_duration < stops[transfer_arr_stop]:
                        stops[transfer_arr_stop] = min(stops[transfer_arr_stop], carr_time + transfer_duration)
                        journey[transfer_arr_stop] = (
                            trips[ctrip_id], (
                            cdep_stop, cdep_time, carr_stop, carr_time, ctrip_id,
                            cmode_transport, route),
                            (transfer_dep_stop, transfer_arr_stop, transfer_duration))

        nbr_connection += 1
    if arrival_time:
        if stops[end_station] > arrival_time:
            return {'journeys': [{}]}

    journey_final = {}
    t = end_station
    while not any(map(lambda ele: ele is None, journey[t])):
        journey_final[t] = journey[t]
        t = journey[t][0][0]

    try:
        start_station_to_t = FootPath.objects.get(transfer_dep_stop__stop_id=start_station, transfer_arr_stop__stop_id=t)
        journey_final[start_station] = (None, None, (
        start_station_to_t.transfer_dep_stop.stop_id, start_station_to_t.transfer_arr_stop.stop_id,
        start_station_to_t.transfer_duration))
    except:
        # If train have a direct connection to the destination
        journey_final[start_station] = (None, None, (start_station, None, 0))

    journey_final = dict(reversed(list(journey_final.items())))

    total_travel_times = stops[end_station] - stops[start_station]

    journeys = extraction_journey(journey_final, total_travel_times, stops[start_station])

    return journeys


def extraction_journey(journey_final, total_travel_times, start_time):
    journeys = [{'journeys': []}]
    result = journeys[0]['journeys']
    for key, val in journey_final.items():
        enter_connection = val[0]
        exit_connection = val[1]
        footpath = val[2]
        if not enter_connection and not exit_connection:
            start_stop = Stop.objects.get(stop_id=footpath[0])
            if footpath[1]:
                end_stop = Stop.objects.get(stop_id=footpath[1])
            else:
                end_stop = start_stop
            result.append({
                'start_station': {
                    'name': start_stop.stop_name,
                    'lat': str(start_stop.stop_lat),
                    'lon': str(start_stop.stop_lon),
                },
                'next_station': [
                    {
                        'name': end_stop.stop_name,
                        'lat': str(end_stop.stop_lat),
                        'lon': str(end_stop.stop_lon),
                    }
                ],
                'footpath': "walking",
                'time_walking': seconds_to_hhmmss(footpath[2]),
                'transport': None,
                'start_time': seconds_to_hhmmss(start_time),
                'end_time': seconds_to_hhmmss(start_time + footpath[2]),
            })
        else:
            next_stations = []
            start_stop = Stop.objects.get(stop_id=enter_connection[0])
            end_stop = Stop.objects.get(stop_id=exit_connection[2])
            end_stop_by_foot = Stop.objects.get(stop_id=footpath[1])
            for stop_times in StopTime.objects.filter(trip=enter_connection[4]).order_by('stop_sequence'):
                next_stations.append(stop_times.stop)

            start_stop_idx = next_stations.index(start_stop)
            end_stop_idx = next_stations.index(end_stop)

            for idx, val in enumerate(next_stations.copy()):
                if idx <= start_stop_idx:
                    next_stations.pop(0)
                elif idx >= end_stop_idx:
                    next_stations.pop(-1)
                else:
                    stop = Stop.objects.get(stop_id=val.stop_id)
                    index = next_stations.index(stop)
                    next_stations[index] = {'name': stop.stop_name, 'lat': str(stop.stop_lat),
                                            'lon': str(stop.stop_lon)}

            result.append({
                'start_station': {
                    'name': start_stop.stop_name,
                    'lat': str(start_stop.stop_lat),
                    'lon': str(start_stop.stop_lon),
                },
                'next_station': next_stations,
                'end_station': {
                    'name': end_stop_by_foot.stop_name,
                    'lat': str(end_stop_by_foot.stop_lat),
                    'lon': str(end_stop_by_foot.stop_lon),
                },
                'transport': enter_connection[6],
                'footpath': "walking",
                'time_walking': seconds_to_hhmmss(footpath[2]),
                'start_time': seconds_to_hhmmss(enter_connection[1]),
                'end_time': seconds_to_hhmmss(exit_connection[3] + footpath[2])
            })

    journeys[0]['total_travel_times'] = seconds_to_hhmmss(total_travel_times)

    return journeys