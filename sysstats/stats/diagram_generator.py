import os

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

C_GREY = '#363737'
C_LIGHT_GREEN = '#26ff55'
C_LIGHT_GREY = '#9c9c9c'
C_WHITE = '#ffffff'

def pie_chart(title: str, data: dict[str, int], autopct):
    labels = []
    sizes = []
    for key, value in data.items():
        labels.append(key)
        sizes.append(value)
    
    labels = labels[::-1]
    sizes = sizes[::-1]

    fig1, ax1 = plt.subplots()
    fig1.set_facecolor(C_GREY)

    wedges, texts, autotexts = ax1.pie(sizes, autopct=autopct, shadow=True, startangle=90, colors=[C_LIGHT_GREY, C_LIGHT_GREEN])
    for autotext in autotexts:
        autotext.set_color('white')
    legend = ax1.legend(wedges, labels, title=title, loc="center left", bbox_to_anchor=(0, 0, 0, 0))
    legend.get_frame().set_facecolor(C_LIGHT_GREY)
    ax1.axis('equal')
    circle = plt.Circle(xy=(0,0), radius=0.85, facecolor=C_GREY)
    fig1.gca().add_artist(circle)
    fig1.savefig(os.path.join("sysstats", "stats", "static", "images", f'{title.lower().replace(" ", "_")}_pie.png'), dpi=200)
    plt.close()

def histogram(title: str, data: dict[str, int], format_str: str = "", max_value: float = 0):
    stat_data = []
    datetimes = []

    for key, value in data.items():
        datetimes.append(key)
        stat_data.append(value)

    fig, axis = plt.subplots()
    axis.plot(datetimes, stat_data, color=C_LIGHT_GREEN, alpha=0.7, linewidth=2.0)

    # formatter = matplotlib.ticker.FormatStrFormatter(format_str)
    locator = mdates.HourLocator(interval=3)
    # axis.xaxis.set_major_formatter(formatter)
    axis.xaxis.set_major_locator(locator)
    axis.margins(x=0, y=0)

    fig.set_facecolor(C_GREY)
    axis.set_facecolor(C_LIGHT_GREY)
    axis.grid(color=C_GREY)
    axis.fill_between(axis.lines[0].get_data()[0], axis.lines[0].get_data()[1], color=C_LIGHT_GREEN, alpha=0.3)
    axis.tick_params(axis='x', colors=C_WHITE)
    axis.tick_params(axis='y', colors=C_WHITE)

    values = []
    labels = []
    max_val = max_value if max_value != 0 else max(data.values())
    for c in range(9):
        values.append((max_val / 8) * c)
        labels.append(_format_size((max_val / 8) * c, format_str))
    plt.yticks(values, labels)

    axis.set_title(label=f'History of {title}', color=C_WHITE)
    if max_value != 0:
        axis.set_ylim(0, max_value)
    fig.savefig(os.path.join("sysstats", "stats", "static", "images", f'{title.lower().replace(" ", "_")}_histogram.png'), dpi=200)
    plt.close()

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
