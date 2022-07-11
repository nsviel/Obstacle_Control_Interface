#! /usr/bin/python
#---------------------------------------------

from param import cla

from src import connection
from src import file
from src import signal
from src import saving


def init():
    file.init_state()
    saving.determine_path()
    connection.start_thread_test_conn()
    cla.contro.status = "Online"

def loop():
    a=1
    #signal.action_keyboard()

def end():
    cla.contro.status = "Offline"
    file.update_state_file()
    connection.stop_thread()
