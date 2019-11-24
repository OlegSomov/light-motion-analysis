import csv
from datetime import datetime
import logging as log


def pretty_print(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return "%dh %02dm %s sec" % (h, m, s)


def get_data(path, event):
    result = []
    try:
        with open(path, "r") as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                result.append({"time": datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'), "value": row[1], "event": event})
    except IndexError:
        log.error("The input data must be two comma separated valued - time and value. Processing {} Error: ".format(path))
        raise
    log.debug("Processed {} readings in file {}".format(len(result), path))
    return result
