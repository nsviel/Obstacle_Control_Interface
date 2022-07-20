#! /usr/bin/python
#---------------------------------------------

from param import param_co
from SOCK import sock_server
from src import connection
from src import signal
from src import saving
from src import image
from src import parser_json


def init():
    saving.determine_path()
    connection.start_daemon()
    sock_server.start_daemon()
    image.start_daemon()
    param_co.state_co["self"]["status"] = "Online"

def loop():
    pass

def end():
    param_co.state_co["self"]["status"] = "Offline"
    parser_json.upload_state()
    connection.stop_daemon()
    sock_server.stop_daemon()
    image.stop_daemon()
