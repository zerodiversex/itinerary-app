from rest_framework.views import APIView
from rest_framework.response import Response
from route_search_engine.connection_scan import connection_scan
from route_search_engine.outils import time_to_seconds
from datetime import datetime
from route_search_engine.models import Stop

class JourneyView(APIView):
    def get(self, request):
        start_station = self.request.query_params.get('start_station')
        end_station = self.request.query_params.get('end_station')
        departure_time = self.request.query_params.get('departure_time')
        arrival_time = self.request.query_params.get('arrival_time')
        if departure_time:
            departure_time_seconds = time_to_seconds(departure_time)
            journeys = connection_scan(start_station, end_station, departure_time=departure_time_seconds, arrival_time=None)
        if arrival_time:
            now = datetime.now()
            departure_time = now.strftime("%H:%M:%S")
            departure_time = time_to_seconds(departure_time)
            arrival_time_seconds = time_to_seconds(arrival_time)
            journeys = connection_scan(start_station, end_station, departure_time=departure_time, arrival_time=arrival_time_seconds)

        return Response(journeys)

class SearchView(APIView):
    def get(self, request):
        stops = []
        search_field = self.request.query_params.get('field')
        stops_query = Stop.objects.filter(stop_name__icontains=search_field)
        for stop in stops_query:
            stops.append({'stop_id': stop.stop_id, 'stop_name': stop.stop_name, 'stop_desc': stop.stop_desc})

        return Response(stops)


