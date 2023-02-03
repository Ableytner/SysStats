import psutil

from stats.models import Record, RamRecord, DriveRecord, NetworkRecord

def get():
    svmem = psutil.virtual_memory()
    ram_record = RamRecord(
        ram_usage=svmem.used,
        ram_total=svmem.total
    )
    ram_record.save()

    disk_data = _get_disk_data()
    last_drive_record = DriveRecord.objects.last()
    drive_record = DriveRecord(
        drive_change=(disk_data["usage"] - last_drive_record.drive_usage) if last_drive_record is not None else 0,
        drive_usage=disk_data["usage"],
        total_drive_size=disk_data["total"]
    )
    drive_record.save()

    snetio = psutil.net_io_counters()
    last_network_record = NetworkRecord.objects.last()
    network_record = NetworkRecord(
        network_up=(snetio.bytes_sent - last_network_record.network_up) if last_network_record is not None else 0,
        network_down=(snetio.bytes_recv - last_network_record.network_down) if last_network_record is not None else 0
    )
    network_record.save()

    record = Record(
        cpu_usage=psutil.cpu_percent(interval=1),
        ram_usage=ram_record,
        drive_usage=drive_record,
        network_usage=network_record
    )
    record.save()

def _get_disk_data() -> dict[str,int]:
    disk_usage = 0
    disk_total = 0
    for disk in psutil.disk_partitions():
        if disk.fstype:
            sdiskusage = psutil.disk_usage(disk.mountpoint)
            disk_usage += sdiskusage.used
            disk_total += sdiskusage.total
    return {"usage":disk_usage,"total":disk_total}
