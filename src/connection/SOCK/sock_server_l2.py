#---------------------------------------------
from src.param import param_control
from src.utils import terminal
from src.base import daemon

import socket


class Socket_l2(daemon.Daemon):
    def thread_init(self):
        port = param_control.state_control["control"]["socket"]["server_l2_port"]
        param_control.sock_server_l2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        param_control.sock_server_l2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        param_control.sock_server_l2.bind(("", port))
        param_control.sock_server_l2.settimeout(1)

    def thread_function(self):
        try:
            packet, (address, port) = param_control.sock_server_l2.recvfrom(4096)
            data.process_l2_data(packet)
            param_control.state_edge["hub"]["socket"]["l2_connected"] = True
        except:
            param_control.state_edge["hub"]["socket"]["l2_connected"] = False

    def thread_end(self):
        param_control.sock_server_l2.close()

    name = "Socket server LiDAR 2";
    run_sleep = 0;
