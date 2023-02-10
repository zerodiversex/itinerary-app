import uuid
from django.db import models
from postgres_copy import CopyManager

class Stop(models.Model):
    stop_id = models.CharField(max_length=255, primary_key=True)
    stop_name = models.CharField(max_length=255)
    stop_desc = models.CharField(max_length=255, blank=True, null=True)
    stop_lat = models.DecimalField(max_digits=15, decimal_places=13)
    stop_lon = models.DecimalField(max_digits=15, decimal_places=13)
    parent_station = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.stop_name}"


class Route(models.Model):
    route_id = models.CharField(max_length=255, primary_key=True)
    route_short_name = models.CharField(max_length=255, blank=True, null=True)
    route_long_name = models.CharField(max_length=255, blank=True, null=True)
    route_desc = models.CharField(max_length=255, blank=True, null=True)
    route_type = models.IntegerField()

    def __str__(self):
        return f"{self.route_short_name} | {self.route_long_name}"


class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    trip_id = models.CharField(max_length=255,  primary_key=True)
    trip_headsign = models.CharField(max_length=255, blank=True, null=True)
    objects = CopyManager()

    def __str__(self):
        return f"{self.route.route_long_name} - {self.trip_headsign}"


class Transfer(models.Model):
    from_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='from_stop')
    to_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='to_stop')
    transfer_type = models.IntegerField()
    min_transfer_time = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.from_stop} to {self.to_stop}'


class StopTime(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    arrival_time = models.IntegerField()
    departure_time = models.IntegerField()
    stop = models.ForeignKey('Stop', on_delete=models.CASCADE)
    stop_sequence = models.IntegerField()
    objects = CopyManager()

    class Meta:
        unique_together = (('trip', 'stop_sequence'),)

    def __str__(self):
        return f"{self.stop.stop_name}"


class Connection(models.Model):
    dep_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='dep_stop')
    dep_time = models.IntegerField()
    arr_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='arr_stop')
    arr_time = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    mode_transport = models.CharField(max_length=255, blank=True, null=True)
    objects = CopyManager()

    def __str__(self):
        return f'{self.dep_stop} to {self.arr_stop}'


class FootPath(models.Model):
    transfer_dep_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='transfer_dep_stop')
    transfer_arr_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='transfer_arr_stop')
    transfer_duration = models.IntegerField(blank=True, null=True)
    objects = CopyManager()

    def __str__(self):
        return f'{self.transfer_dep_stop} to {self.transfer_arr_stop}'
