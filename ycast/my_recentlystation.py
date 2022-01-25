import logging

import yaml
from ycast import generic

MAX_ENTRIES = 15

recently_file = generic.get_var_path() + '/recently.yml'


def signal_station_selected(name, url, icon):
    logging.debug("  %s:%s|%s", name, url, icon)
    list_heard_stations = get_stations_list()
    if len(list_heard_stations) == 0:
        list_heard_stations.append("recently used:\n")
    # make name yaml - like
    name = name.replace(":", " -")

    for line in list_heard_stations:
        elements = line.split(': ')
        if elements[0] == '  '+name:
            list_heard_stations.remove(line)
            logging.debug("Name '%s' exists and deleted", name)
    piped_icon = ''
    if icon and len(icon) > 0:
        piped_icon = '|' + icon

    list_heard_stations.insert(1, '  '+name+': '+url+piped_icon+'\n')
    if len(list_heard_stations) > MAX_ENTRIES+1:
        # remove last (oldest) entry
        list_heard_stations.pop()

    set_stations_yaml(list_heard_stations)


def set_stations_yaml(heard_stations):
    try:
        with open(recently_file, 'w') as f:
            f.writelines(heard_stations)
            logging.info("File written '%s'", recently_file)

    except Exception as ex:
        logging.error("File not written '%s': %s", recently_file, ex)


def get_stations_list():
    try:
        with open(recently_file, 'r') as f:
            heard_stations = f.readlines()
    except FileNotFoundError:
        logging.warning("File not found '%s' not found", recently_file)
        return []
    except yaml.YAMLError as e:
        logging.error("Station configuration format error: %s", e)
        return []
    return heard_stations


def get_recently_stations_yaml():
    try:
        with open(recently_file, 'r') as f:
            my_stations = yaml.safe_load(f)
    except FileNotFoundError:
        logging.error("Station configuration '%s' not found", recently_file)
        return None
    except yaml.YAMLError as e:
        logging.error("Station configuration format error: %s", e)
        return None
    return my_stations
