from route_search_engine.models import Stop, Route, Trip, Transfer, StopTime, Connection, FootPath
from django.core.management.base import BaseCommand
from route_search_engine.outils import time_to_seconds, KeyList, seconds_to_hhmmss, haversine_distance
import requests
import csv
import math


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.import_stops()
        self.import_routes()
        self.import_trips()
        self.import_transfer()
        self.import_stop_times()
        self.import_connections()
        self.import_footpath()

    def import_stops(self):
        print("Importing stops...")
        url = "https://storage.googleapis.com/gtfs_data/stops.txt"
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines[1:]:
                line_split = line.split(',')
                stop_id = line_split[0]
                stop_name = line_split[1].encode('latin1').decode('utf8')
                stop_lat = line_split[2]
                stop_lon = line_split[3]
                parent_station = line_split[5]
                if parent_station != '':
                    stop = Stop.objects.create(stop_id=stop_id, stop_name=stop_name,
                                               stop_lat=stop_lat, stop_lon=stop_lon, parent_station=parent_station)
                else:
                    stop = Stop.objects.create(stop_id=stop_id, stop_name=stop_name,
                                               stop_lat=stop_lat, stop_lon=stop_lon)
                stop.save()
            print(f"Finished importing {Stop.objects.count()} stops.")
        else:
            print("Status code:", response.status_code)

    def import_routes(self):
        print("Importing routes...")
        url = "https://storage.googleapis.com/gtfs_data/routes.txt"
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines[1:]:
                line_split = line.split(',')
                route_id = line_split[0]
                route_short_name = line_split[2]
                route_long_name = line_split[3]
                route_type = line_split[5]
                route_desc = line_split[4]
                route = Route.objects.create(route_id=route_id, route_short_name=route_short_name,
                                             route_long_name=route_long_name, route_type=route_type, route_desc=route_desc)
                route.save()
            print(f"Finished importing {Route.objects.count()} routes.")
        else:
            print("Status code:", response.status_code)

    def import_trips(self):
        print("Importing trips...")
        url = "https://storage.googleapis.com/gtfs_data/trips.txt"
        response = requests.get(url)
        headers = ['route', 'trip_id', 'trip_headsign']
        rows = []
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines[1:]:
                line_split = line.split(',')
                route_id = line_split[0]
                trip_id = line_split[2]
                trip_headsign = line_split[3]
                rows.append({
                    'route': route_id,
                    'trip_id': trip_id,
                    'trip_headsign': trip_headsign
                })
        with open('trips.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        Trip.objects.from_csv(
            "trips.csv",  # The path to a source file (a Python file object is also acceptable)
            # A crosswalk of model fields to CSV headers.
            dict(route='route', trip_id='trip_id', trip_headsign='trip_headsign')
        )

    def import_transfer(self):
        print("Importing transfers...")
        url = "https://storage.googleapis.com/gtfs_data/transfers.txt"
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines[1:]:
                line_split = line.split(',')
                from_stop_id = line_split[0]
                to_stop_id = line_split[1]
                transfer_type = line_split[2]
                min_transfer_time = line_split[3]
                if transfer_type == "2":
                    transfer = Transfer.objects.create(
                        from_stop_id=from_stop_id, to_stop_id=to_stop_id, transfer_type=transfer_type, min_transfer_time=min_transfer_time)
                    transfer.save()
            print("Finished importing transfers.")
        else:
            print("Status code:", response.status_code)

    def import_stop_times(self):
        print("Importing stops time...")
        url = "https://storage.googleapis.com/gtfs_data/stop_times.txt"
        response = requests.get(url)
        headers = ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence']
        rows = []
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines[1:]:
                line_split = line.split(',')
                trip_id = line_split[0]
                arr_time = int(time_to_seconds(line_split[1]))
                dep_time = int(time_to_seconds(line_split[2]))
                stop_id = line_split[3]
                stop_sequence = int(line_split[4])
                rows.append({
                    'trip_id': trip_id,
                    'arrival_time': arr_time,
                    'departure_time': dep_time,
                    'stop_id': stop_id,
                    'stop_sequence': stop_sequence,
                })
        with open('stop_times.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        StopTime.objects.from_csv("stop_times.csv", dict(stop='stop_id', trip='trip_id',
                                  arrival_time='arrival_time', departure_time='departure_time', stop_sequence='stop_sequence'))

    def import_footpath(self):
        print(f"Importing footpaths...")
        headers = ['transfer_dep_stop', 'transfer_arr_stop', 'transfer_duration']
        rows = []
        for from_stop in Stop.objects.all().values_list('stop_id', 'stop_lat', 'stop_lon'):
            from_stop_id = from_stop[0]
            from_stop_lat = from_stop[1]
            from_stop_lon = from_stop[2]
            print(f"Importing footpaths from {from_stop_id}...")
            for to_stop in Stop.objects.all().values_list('stop_id', 'stop_lat', 'stop_lon'):
                to_stop_id = to_stop[0]
                to_stop_lat = to_stop[1]
                to_stop_lon = to_stop[2]
                if from_stop_id != to_stop_id:
                    transfer_time = haversine_distance(from_stop_lat, from_stop_lon, to_stop_lat, to_stop_lon)
                    if transfer_time <= 5 * 60:
                        rows.append({
                            'transfer_dep_stop': from_stop_id,
                            'transfer_arr_stop': to_stop_id,
                            'transfer_duration': transfer_time,
                        })
                else:
                    rows.append({
                        'transfer_dep_stop': from_stop_id,
                        'transfer_arr_stop': to_stop_id,
                        'transfer_duration': Transfer.objects.get(from_stop_id=from_stop_id, to_stop_id=to_stop_id).min_transfer_time,
                    })

        with open('footpaths.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        FootPath.objects.from_csv("footpaths.csv", dict(transfer_dep_stop='transfer_dep_stop', transfer_arr_stop='transfer_arr_stop',
                                                        transfer_duration='transfer_duration'))

        print(f"Finish importing {FootPath.objects.count()} footpaths...")

    def import_connections(self):
        print("Importing connections...")
        headers = ['dep_stop', 'dep_time', 'arr_stop', 'arr_time', 'trip', 'route', 'mode_transport']
        rows = []
        trip_queryset = Trip.objects.all().values_list('trip_id', 'route_id', 'route__route_type')
        j = 0
        for trip_id, route_id, route_type in trip_queryset:
            stop_times_queryset = StopTime.objects.filter(trip=trip_id).order_by(
                'stop_sequence').values_list('stop_id', 'arrival_time', 'departure_time')
            for i, stop_time in enumerate(stop_times_queryset):
                if i > 0:
                    rows.append({
                        'dep_stop': stop_times_queryset[i-1][0],
                        'dep_time': int(stop_times_queryset[i-1][2]),
                        'arr_stop': stop_time[0],
                        'arr_time': int(stop_time[1]),
                        'trip': trip_id,
                        'route': route_id,
                        'mode_transport': route_type,
                    })
            j += 1
        with open('connections.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        Connection.objects.from_csv("connections.csv", dict(dep_stop='dep_stop', arr_stop='arr_stop',
                                                            dep_time='dep_time', arr_time='arr_time',
                                                            trip='trip', route='route', mode_transport='mode_transport'))

        print(f"Finished importing {Connection.objects.count()} connections.")
