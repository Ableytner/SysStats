from django.shortcuts import render, HttpResponse, redirect
from django.template.defaulttags import register
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now

from datetime import datetime, timedelta

from stats import diagram_generator, stat_getter
from stats.models import Record

@login_required(login_url='/accounts/login/')
def index(request):
    stats = stat_getter.update()
    _gen_cpu_usage_diagram(stats)
    _gen_ram_usage_diagram(stats)
    _gen_drive_usage_diagram(stats)
    return render(request, "stats/index.html")

@login_required(login_url='/accounts/login/')
def history(request):
    _gen_cpu_history_diagram()
    _gen_ram_history_diagram()
    _gen_drive_history_diagram()
    _gen_network_history_diagram()
    return render(request, "stats/history.html")

def _gen_cpu_usage_diagram(stats):
    data = {
        "Used": (stats["cpu"]),
        "Unused": (100 - stats["cpu"])
    }

    def my_autopct(val):
        return f"{int(round(val,0))}%"

    diagram_generator.pie_chart("CPU Usage", data, my_autopct)

def _gen_ram_usage_diagram(stats):
    data = {
        "Used": (stats["ram_u"]),
        "Free": (stats["ram_t"] - stats["ram_u"])
    } 

    def make_autopct(total):
        def my_autopct(val):
            return f"{round(val, 1)}%\n{_format_size(total*(val/100))}"
        return my_autopct

    diagram_generator.pie_chart("RAM Usage", data, make_autopct(stats["ram_t"]))

def _gen_drive_usage_diagram(stats):
    data = {
        "Used": (stats["disk_u"]),
        "Free": (stats["disk_t"] - stats["disk_u"])
    }

    def make_autopct(total):
        def my_autopct(val):
            return f"{round(val, 1)}%\n{_format_size(total*(val/100))}"
        return my_autopct

    diagram_generator.pie_chart("Drive Usage", data, make_autopct(stats["disk_t"]))

def _gen_cpu_history_diagram():
    data = {}
    for stat in Record.objects.filter(record_date__gte=(now() - timedelta(days=1))):
        try:
            data[stat.record_date] = stat.cpu_usage
        except ObjectDoesNotExist:
            pass

    diagram_generator.histogram("CPU Usage", data, format_str='%.1f%%', max_value=100.0)

def _gen_ram_history_diagram():
    data = {}
    for stat in Record.objects.filter(record_date__gte=(now() - timedelta(days=1))):
        try:
            data[stat.record_date] = stat.ram_usage.ram_usage
        except ObjectDoesNotExist:
            pass

    diagram_generator.histogram("RAM Usage", data, max_value=Record.objects.last().ram_usage.ram_total)

def _gen_drive_history_diagram():
    data = {}
    for stat in Record.objects.filter(record_date__gte=(now() - timedelta(days=1))):
        try:
            data[stat.record_date] = stat.drive_usage.drive_usage
        except ObjectDoesNotExist:
            pass

    diagram_generator.histogram("Drive Usage", data, max_value=Record.objects.last().drive_usage.total_drive_size)

def _gen_network_history_diagram():
    data_up = {}
    data_down = {}
    for stat in Record.objects.filter(record_date__gte=(now() - timedelta(days=1))):
        try:
            data_up[stat.record_date] = stat.network_usage.network_up
            data_down[stat.record_date] = stat.network_usage.network_down
        except ObjectDoesNotExist:
            pass

    diagram_generator.histogram("Network Upload", data_up)
    diagram_generator.histogram("Network Download", data_down)

def _format_size(bytes, format_str=""):
    """
    Returns size of bytes in a nice format
    """
    if format_str != "":
        return format_str % bytes

    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
