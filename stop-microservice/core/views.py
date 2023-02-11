from rest_framework.views import APIView
from rest_framework.response import Response
from core.connection_scan import connection_scan
from core.outils import time_to_seconds
from datetime import datetime
from core.models import Stop


class StopView(APIView):
    def get(self, request):
        stops = []
        search_field = self.request.query_params.get('search')
        stops_query = Stop.objects.filter(stop_name__icontains=search_field)
        for stop in stops_query:
            stops.append({'stop_id': stop.stop_id, 'stop_name': stop.stop_name, 'stop_desc': stop.stop_desc})

        return Response(stops)


