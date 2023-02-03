from django.db import models
from django.core.validators import MinValueValidator

class RamRecord(models.Model):
    ram_usage = models.IntegerField(validators=[MinValueValidator(0)])
    ram_total = models.IntegerField(validators=[MinValueValidator(0)])

class DriveRecord(models.Model):
    drive_change = models.IntegerField(null=True)
    drive_usage = models.IntegerField(validators=[MinValueValidator(0)])
    total_drive_size = models.IntegerField(validators=[MinValueValidator(0)])

class NetworkRecord(models.Model):
    network_down = models.IntegerField(validators=[MinValueValidator(0)])
    network_up = models.IntegerField(validators=[MinValueValidator(0)])

class Record(models.Model):
    cpu_usage = models.IntegerField(validators=[MinValueValidator(0)])
    ram_usage = models.OneToOneField(RamRecord, on_delete=models.CASCADE)
    drive_usage = models.OneToOneField(DriveRecord, on_delete=models.CASCADE)
    network_usage = models.OneToOneField(NetworkRecord, on_delete=models.CASCADE)
    record_date = models.DateTimeField(auto_now_add=True, blank=True)
