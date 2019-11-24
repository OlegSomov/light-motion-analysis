from datetime import datetime, timedelta
import json


class LightModel:
    # class to keep track of the light model

    def __init__(self):
        self.last_on = datetime(1970, 1, 1)
        self.total_on = 0
        self.light_states = []
        self.state = False

    def add_on(self, date, offset):
        # add a record when the light was ON
        self.light_states.append({
            'x': (date - timedelta(seconds=offset)).strftime("%Y-%m-%d %H:%M:%S"),
            'y': 0})
        self.light_states.append(
            {'x': date.strftime("%Y-%m-%d %H:%M:%S"), 'y': 1})
        self.state = True
        self.last_on = date

    def add_off(self, date, offset):
        self.light_states.append({
            'x': (date - timedelta(seconds=offset)).strftime("%Y-%m-%d %H:%M:%S"),
            'y': 1})
        # add a record when the time was OFF
        self.light_states.append(
            {'x': date.strftime("%Y-%m-%d %H:%M:%S"), 'y': 0})
        # calculate how much time the light was ON
        self.total_on += (date - self.last_on).seconds
        self.state = False

    def is_on(self):
        return self.state

    def save_to_json(self, name):
        with (open(name, 'w')) as f:
            json.dump(self.light_states, f)
