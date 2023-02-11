from rest_framework.views import APIView
from rest_framework.response import Response
from core.raptor import connection_scan
from core.outils import time_to_seconds
from datetime import datetime

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

