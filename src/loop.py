#---------------------------------------------
from param import param_co
from SOCK import sock_server
from src import connection
from src import signal
from src import saving
from src import image
from src import parser_json
from src import state
from src import wallet

import time


def init():
    saving.determine_path()
    connection.start_daemon()
    sock_server.start_daemon()
    image.start_daemon()
    print("[\033[1;32mOK\033[0m] Program initialized...")

def loop():
    time.sleep(0.01)

def end():
    print("[\033[1;32mOK\033[0m] Program terminating...")
    parser_json.upload_state()
    connection.stop_daemon()
    sock_server.stop_daemon()
    image.stop_daemon()
    time.sleep(2)
