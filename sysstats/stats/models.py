from django.db import models
from django.core.validators import MinValueValidator

class RamRecord(models.Model):
    ramrecord_id = models.IntegerField(primary_key=True)
    ram_usage = models.IntegerField(validators=[MinValueValidator(0)])
    ram_total = models.IntegerField(validators=[MinValueValidator(0)])

class DriveRecord(models.Model):
    driverecord_id = models.IntegerField(primary_key=True)
    drive_usage = models.IntegerField(validators=[MinValueValidator(0)])
    total_drive_size = models.IntegerField(validators=[MinValueValidator(0)])

class NetworkRecord(models.Model):
    networkrecord_id = models.IntegerField(primary_key=True)
    network_down = models.IntegerField(validators=[MinValueValidator(0)])
    network_up = models.IntegerField(validators=[MinValueValidator(0)])

class Record(models.Model):
    cpu_usage = models.IntegerField(validators=[MinValueValidator(0)])
    ram_usage = models.ForeignKey(RamRecord, on_delete=models.CASCADE)
    drive_usage = models.ForeignKey(DriveRecord, on_delete=models.CASCADE)
    network_usage = models.ForeignKey(NetworkRecord, on_delete=models.CASCADE)
    record_date = models.DateTimeField('date published')
