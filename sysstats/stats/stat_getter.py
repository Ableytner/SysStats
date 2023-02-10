from django.utils.timezone import now

from datetime import datetime, timedelta
from time import sleep
import os

import stats.getter_win as getter_win
from stats.models import Record, RamRecord, DriveRecord, NetworkRecord

UPDATE_DELAY = 60 # 1 minute

def update() -> dict:
    if os.name == "nt":
        return getter_win.get(UPDATE_DELAY)
    else:
        raise Exception("Linux is not supported!")

def _update_func() -> None:
    while True:
        start_time = datetime.now()

        stats = update()
        _save_stats(stats)

        _cleanup_database()
        
        sleep(UPDATE_DELAY - (datetime.now() - start_time).seconds)

def _save_stats(stats) -> None:
    ram_record = RamRecord(
        ram_usage=stats["ram_u"],
        ram_total=stats["ram_t"]
    )
    ram_record.save()

    last_drive_record = DriveRecord.objects.last()
    drive_record = DriveRecord(
        drive_change=(stats["disk_u"] - last_drive_record.drive_usage) if last_drive_record is not None else 0,
        drive_usage=stats["disk_u"],
        total_drive_size=stats["disk_t"]
    )
    drive_record.save()

    network_record = NetworkRecord(
        network_up=stats["netw_s"],
        network_down=stats["netw_r"],
        network_up_total=stats["netw_s_t"],
        network_down_total=stats["netw_r_t"]
    )
    network_record.save()

    record = Record(
        cpu_usage=stats["cpu"],
        ram_usage=ram_record,
        drive_usage=drive_record,
        network_usage=network_record
    )
    record.save()

def _cleanup_database() -> None:
    for record in Record.objects.filter(record_date__lte=(now() - timedelta(days=1))):
        record.delete(keep_parents=False)
