import psutil

from stats.models import NetworkRecord

def get(UPDATE_DELAY: int):
    svmem = psutil.virtual_memory()

    disk_data = _get_disk_data()

    snetio = psutil.net_io_counters()
    last_network_record = NetworkRecord.objects.last()
    if last_network_record is None or \
       (last_network_record.network_up_total > snetio.bytes_sent and \
        last_network_record.network_down_total > snetio.bytes_recv):
        netw_up = 0
        netw_down = 0
    else:
        netw_up = int((snetio.bytes_sent - last_network_record.network_up_total) / UPDATE_DELAY)
        netw_down = int((snetio.bytes_recv - last_network_record.network_down_total) / UPDATE_DELAY)

    stats = {
        "cpu": psutil.cpu_percent(interval=1),
        "ram_u": svmem.used,
        "ram_t": svmem.total,
        "disk_u": disk_data["usage"],
        "disk_t": disk_data["total"],
        "netw_s": netw_up,
        "netw_r": netw_down,
        "netw_s_t": snetio.bytes_sent,
        "netw_r_t": snetio.bytes_recv
    }
    # print("Adding stats", stats)
    return stats

def _get_disk_data() -> dict[str,int]:
    disk_usage = 0
    disk_total = 0
    for disk in psutil.disk_partitions():
        if disk.fstype:
            sdiskusage = psutil.disk_usage(disk.mountpoint)
            disk_usage += sdiskusage.used
            disk_total += sdiskusage.total
    return {"usage":disk_usage,"total":disk_total}
