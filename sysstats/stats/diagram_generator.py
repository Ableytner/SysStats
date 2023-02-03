import os

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

BACKGROUND_COLOR = '#363737'
DIAGRAM_GREEN_COLOR = '#26ff55'
DIAGRAM_GRAY_COLOR = '#9c9c9c'

def pie_chart(title: str, data: dict[str, int], autopct):
    labels = []
    sizes = []
    for key, value in data.items():
        labels.append(key)
        sizes.append(value)
    
    labels = labels[::-1]
    sizes = sizes[::-1]

    fig1, ax1 = plt.subplots()
    fig1.set_facecolor(BACKGROUND_COLOR)

    wedges, texts, autotexts = ax1.pie(sizes, autopct=autopct, shadow=True, startangle=90, colors=[DIAGRAM_GRAY_COLOR, DIAGRAM_GREEN_COLOR])
    for autotext in autotexts:
        autotext.set_color('white')
    legend = ax1.legend(wedges, labels, title=title, loc="center left", bbox_to_anchor=(0, 0, 0, 0))
    legend.get_frame().set_facecolor(DIAGRAM_GRAY_COLOR)
    ax1.axis('equal')
    circle = plt.Circle(xy=(0,0), radius=0.85, facecolor=BACKGROUND_COLOR)
    plt.gca().add_artist(circle)
    plt.savefig(os.path.join("sysstats", "stats", "static", "images", f'{title.lower().replace(" ", "_")}.png'),dpi=200)
