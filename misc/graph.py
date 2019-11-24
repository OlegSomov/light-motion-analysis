import os
import matplotlib
import json
from datetime import datetime
from matplotlib import pyplot


def show_results_graph(timer, name=None):
    with (open('light_plot.json', 'r')) as f:
        data = json.load(f)

    with (open('light_plot_imporved.json', 'r')) as f:
        data_improved = json.load(f)

    os.remove('light_plot.json')
    os.remove('light_plot_imporved.json')
    x = []
    y = []
    x_improved = []
    y_improved = []

    for item in data:
        date = datetime.strptime(item['x'], "%Y-%m-%d %H:%M:%S")
        x.append(date)
        if item['y'] == 1:
            y.append(item['y'] + 0.1)  # to distinct normal light and improved light states
        else:
            y.append(item['y'])

    for item in data_improved:
        date = datetime.strptime(item['x'], "%Y-%m-%d %H:%M:%S")
        x_improved.append(date)
        y_improved.append(item['y'])

    dates_normal = matplotlib.dates.date2num(x)
    dates_improved = matplotlib.dates.date2num(x_improved)

    matplotlib.pyplot.plot_date(dates_normal, y, 'b-', label="Regular data", linewidth=2)
    matplotlib.pyplot.plot_date(dates_improved, y_improved, 'b-', color="red", label="Possible improvement", linewidth=2)
    pyplot.title("Compare actual data and possible improvement ({} minutes)".format(timer))
    pyplot.legend()
    if name:
        pyplot.savefig("result.png")
    pyplot.show()
