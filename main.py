import numpy as np
from sklearn.cluster import KMeans

from datetime import datetime, timedelta
from light_model import LightModel
from misc.helpers import pretty_print, get_data
from misc.graph import show_results_graph
import logging as log

log.basicConfig(level=log.INFO)

IMPROVED_TIMER = 5 * 60  # seconds
SETTLE_TIME = 30  # seconds to prevent state flipping

# combine time series data into one list. Event 2 - light reading, 0 - PIR reading
light_sensor = get_data("data/light.csv", "2")
pir_sensor = get_data("data/pir.csv", "0")

# cluster light readings to determine if light is on or off
clusters = KMeans(n_clusters=2).fit(np.array([i["value"] for i in light_sensor]).reshape(-1, 1))

# find an index of the cluster where the light is ON
on_index = list(clusters.cluster_centers_).index(max(clusters.cluster_centers_))


# define function to determine if the reading means light is ON or OFF
def light_state_on(reading):
    if clusters.predict(np.array(reading).reshape(-1, 1)) == on_index:
        return True
    return False


# order a list in chronological order and use time as the key
ordered = sorted(light_sensor + pir_sensor, key=lambda k: k["time"])

normal_light = LightModel()
improved_light = LightModel()
last_move = datetime(1970, 1, 1)

for entry in ordered:
    curr_date = entry["time"]
    if entry['event'] == "2":
        if not light_state_on(entry['value']):  # check if light is OFF
            if normal_light.is_on() and (curr_date - normal_light.last_on).seconds > SETTLE_TIME:
                # more than 30 sec means it was indeed off update last off
                normal_light.add_off(curr_date, SETTLE_TIME)
                log.debug("Total time ON: {}. Between {} and {}".format(pretty_print((curr_date - normal_light.last_on).seconds - SETTLE_TIME),
                                                                        normal_light.last_on, curr_date))
        else:
            # light is on
            if not normal_light.is_on():
                normal_light.add_on(curr_date, SETTLE_TIME)

            if improved_light.is_on() and (curr_date - last_move).seconds > IMPROVED_TIMER:
                improved_off_time = last_move + timedelta(seconds=IMPROVED_TIMER)
                improved_light.add_off(improved_off_time, SETTLE_TIME)
                log.debug("Improved time ON: {}. Between {} and {}".format(pretty_print((improved_off_time - improved_light.last_on).seconds),
                                                                           improved_light.last_on, improved_off_time))
    if entry['event'] == "0":
        if (int(entry['value']) == 1):
            # the improved light is OFF
            if not improved_light.is_on() and normal_light.is_on():
                improved_light.add_on(curr_date, SETTLE_TIME)
            last_move = curr_date

log.info("Total time lights were ON: {} seconds".format(pretty_print(normal_light.total_on)))
log.info('Possible time ON ({} min timer): {}'.format(IMPROVED_TIMER / 60, pretty_print(improved_light.total_on)))
log.info("Improvement {}%".format((normal_light.total_on - improved_light.total_on) * 100 / normal_light.total_on))

# save data for graph
normal_light.save_to_json("light_plot.json")
improved_light.save_to_json("light_plot_imporved.json")

show_results_graph(IMPROVED_TIMER / 60, "results.png")
