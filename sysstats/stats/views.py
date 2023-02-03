from django.shortcuts import render, HttpResponse, redirect
from django.template.defaulttags import register
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from stats import diagram_generator, stat_getter
from stats.models import Record

@login_required(login_url='/accounts/login/')
def index(request):
    stat_getter.update()
    _gen_cpu_usage_diagram()
    _gen_ram_usage_diagram()
    _gen_drive_usage_diagram()
    return render(request, "stats/index.html")

def _gen_cpu_usage_diagram():
    record = Record.objects.last()
    data = {
        "Used": (record.cpu_usage),
        "Unused": (100 - record.cpu_usage)
    }

    def my_autopct(val):
        return f"{int(round(val,0))}%"

    diagram_generator.pie_chart("CPU Usage", data, my_autopct)

def _gen_ram_usage_diagram():
    ram_record = Record.objects.last().ram_usage
    data = {
        "Used": (ram_record.ram_usage * 10**-9),
        "Free": ((ram_record.ram_total - ram_record.ram_usage) * 10**-9)
    } 

    def make_autopct(total):
        def my_autopct(val):
            return f"{round(val, 1)}%\n{str(round(total*(val/100), 1))} GB"
        return my_autopct

    diagram_generator.pie_chart("RAM Usage", data, make_autopct(ram_record.ram_total * 10**-9))

def _gen_drive_usage_diagram():
    drive_record = Record.objects.last().drive_usage
    data = {
        "Used": (drive_record.drive_usage * 10**-12),
        "Free": ((drive_record.total_drive_size - drive_record.drive_usage) * 10**-12)
    } 

    def make_autopct(total):
        def my_autopct(val):
            return f"{round(val, 1)}%\n{str(round(total*(val/100), 3))} TB"
        return my_autopct

    diagram_generator.pie_chart("Drive Usage", data, make_autopct(drive_record.total_drive_size * 10**-12))

def history(request):
    disk_context = {
        "colors": ['#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'],
        "labels": ["used", "free"],
        "data": [1703, 795],
    }
    return render(request, "stats/pie_chart.html", disk_context)
