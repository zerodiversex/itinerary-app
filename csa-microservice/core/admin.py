from django.contrib import admin
from route_search_engine.models import Stop, Route, Trip, Transfer, StopTime, Connection, FootPath
from route_search_engine.outils import seconds_to_hhmmss

class StopAdmin(admin.ModelAdmin):
    list_display = ('stop_id', 'stop_name', 'stop_desc')
    ordering = ('stop_id',)
    search_fields = ('stop_id', 'stop_name',)

class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_id', 'route_short_name', 'route_long_name', 'route_desc', 'route_type')
    ordering = ('route_id', 'route_type')
    search_fields = ('route_id',)

class TripAdmin(admin.ModelAdmin):
    list_display = ('route', 'trip_id', 'trip_headsign',)
    ordering = ('route', 'trip_id', 'trip_headsign')
    search_fields = ('route', 'trip_id',)

class TransferAdmin(admin.ModelAdmin):
    list_display = ('from_stop', 'to_stop', 'transfer_type', 'min_transfer_time')
    ordering = ('from_stop', 'transfer_type')
    search_fields = ('from_stop', 'to_stop', 'transfer_type',)

class StopTimeAdmin(admin.ModelAdmin):
    list_display = ('trip', 'get_arr_time', 'get_dep_time', 'stop', 'stop_sequence', 'get_routes',)
    ordering = ('trip', 'departure_time', 'arrival_time')
    search_fields = ('trip', 'departure_time', 'arrival_time', 'stop', 'stop_sequence', 'get_routes',)

    def get_dep_time(self, obj):
        return f"{seconds_to_hhmmss(obj.departure_time)}"

    def get_arr_time(self, obj):
        return f"{seconds_to_hhmmss(obj.arrival_time)}"

    def get_routes(self, obj):
        return f"{obj.trip.route.route_long_name} | {obj.trip.trip_headsign} "


class FootPathAdmin(admin.ModelAdmin):
    list_display = ('transfer_dep_stop', 'transfer_arr_stop', 'transfer_duration')
    ordering = ('transfer_dep_stop', 'transfer_arr_stop', 'transfer_duration')
    search_fields = ('transfer_dep_stop', 'transfer_arr_stop', 'transfer_duration',)


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('dep_stop', 'arr_stop', 'get_dep_time', 'get_arr_time', 'mode_transport', 'get_trips',)
    ordering = ('dep_stop', 'arr_stop', 'dep_time', 'arr_time', 'mode_transport',)
    search_fields = ('dep_stop', 'arr_stop', 'dep_time', 'arr_time', 'mode_transport',)

    def get_dep_time(self, obj):
        return f"{seconds_to_hhmmss(obj.dep_time)}"

    def get_arr_time(self, obj):
        return f"{seconds_to_hhmmss(obj.arr_time)}"

    def get_trips(self, obj):
        return f"{obj.trip.trip_headsign} | {obj.trip.trip_id} "


admin.site.register(Stop, StopAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(StopTime, StopTimeAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(FootPath, FootPathAdmin)