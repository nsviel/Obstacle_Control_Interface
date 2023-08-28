#---------------------------------------------
from src.param import param_control
from src.base import node
from src.element.edge.ai import ai_node
from src.element.edge.data import data_node
from src.element.edge.slam import slam_node
from src.gui.style import colorization
from src.gui.style import gui_color
from src.utils import parser_json
from src.connection.HTTPS import https_client_post
import dearpygui.dearpygui as dpg


class Hub_node(node.Node):
    # Build function
    def build(self):
        self.ID.init_ID_icon()
        with dpg.node(label=self.ID.name, tag=self.ID.ID_node):
            # Icone & status button
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                with dpg.table(header_row=False, borders_innerH=False, policy=dpg.mvTable_SizingStretchProp, width=100):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    with dpg.table_row():
                        dpg.add_image(self.ID.ID_icon_hub, width=15, height=15)
                        dpg.add_button(tag=self.ID.ID_status_light, width=15)
                with dpg.drawlist(width=100, height=1):
                    dpg.draw_line([0, 0], [125, 0], color=gui_color.color_line)

            # Edge info
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                with dpg.group(horizontal=True):
                    dpg.add_text("Edge ID: [")
                    dpg.add_text("", tag=self.ID.ID_edge_id, color=gui_color.color_node_sub)
                    dpg.add_text("]")
                with dpg.group(horizontal=True):
                    dpg.add_text("Country: [")
                    dpg.add_text("", tag=self.ID.ID_edge_country, color=gui_color.color_node_sub)
                    dpg.add_text("]")
                with dpg.drawlist(width=100, height=1):
                    dpg.draw_line([0, 0], [125, 0], color=gui_color.color_line)

            # MQTT
            with dpg.node_attribute(tag=self.ID.ID_mqtt_client, attribute_type=dpg.mvNode_Attr_Output, shape=dpg.mvNode_PinShape_QuadFilled):
                with dpg.group(horizontal=True):
                    dpg.add_text("MQTT");
                    dpg.add_text("client", color=gui_color.color_node_sub);
                    dpg.add_input_text(tag=self.ID.ID_mqtt_client_name, default_value="ai_module", width=90, on_enter=True, callback=self.command_mqtt)
                dpg.add_button(label="False alarm", callback=self.command_false_alarm)
                with dpg.drawlist(width=100, height=1):
                    dpg.draw_line([0, 0], [125, 0], color=gui_color.color_line)

            # Socket - lidar 1
            with dpg.node_attribute(tag=self.ID.ID_sock_server_l1, attribute_type=dpg.mvNode_Attr_Input, shape=dpg.mvNode_PinShape_QuadFilled):
                with dpg.group(horizontal=True):
                    dpg.add_text("Socket");
                    dpg.add_text("server", color=gui_color.color_node_sub);
                    dpg.add_input_int(tag=self.ID.ID_sock_server_l1_port, default_value=1, width=75, callback=self.command_port_socket);
            with dpg.node_attribute(tag=self.ID.ID_sock_client_l1, attribute_type=dpg.mvNode_Attr_Output, shape=dpg.mvNode_PinShape_QuadFilled):
                with dpg.group(horizontal=True):
                    dpg.add_text("Socket");
                    dpg.add_text("client", color=gui_color.color_node_sub);
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                with dpg.group(horizontal=True):
                    dpg.add_text("Source:");
                    choice = ("lidar_1", "lidar_2")
                    dpg.add_combo(choice, tag=self.ID.ID_combo_lidar_source, label="", default_value="Lidar 1", width=75, callback=self.command_combo_lidar_main)
                with dpg.drawlist(width=100, height=1):
                    dpg.draw_line([0, 0], [125, 0], color=gui_color.color_line)

            # Socket - lidar 2
            with dpg.node_attribute(tag=self.ID.ID_sock_server_l2, attribute_type=dpg.mvNode_Attr_Input, shape=dpg.mvNode_PinShape_QuadFilled):
                with dpg.group(horizontal=True):
                    dpg.add_text("Socket");
                    dpg.add_text("server", color=gui_color.color_node_sub);
                    dpg.add_input_int(tag=self.ID.ID_sock_server_l2_port, default_value=1, width=75, callback=self.command_port_socket);
            with dpg.node_attribute(tag=self.ID.ID_sock_client_l2, attribute_type=dpg.mvNode_Attr_Output, shape=dpg.mvNode_PinShape_QuadFilled):
                with dpg.group(horizontal=True):
                    dpg.add_text("Socket");
                    dpg.add_text("client", color=gui_color.color_node_sub);
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                with dpg.group(horizontal=True):
                    dpg.add_text("Source:");
                    dpg.add_text("Lidar 2", tag=self.ID.ID_sock_client_l2_source)
                with dpg.drawlist(width=100, height=1):
                    dpg.draw_line([0, 0], [125, 0], color=gui_color.color_line)

            # HTTP
            with dpg.node_attribute(tag=self.ID.ID_http_client, attribute_type=dpg.mvNode_Attr_Output, shape=dpg.mvNode_PinShape_QuadFilled):
                with dpg.group(horizontal=True):
                    dpg.add_text("HTTPS");
                    dpg.add_text("client", color=gui_color.color_node_sub);
            with dpg.node_attribute(tag=self.ID.ID_http_server, attribute_type=dpg.mvNode_Attr_Output, shape=dpg.mvNode_PinShape_QuadFilled):
                with dpg.group(horizontal=True):
                    dpg.add_text("HTTPS");
                    dpg.add_text("server", color=gui_color.color_node_sub);
                    dpg.add_text(1, tag=self.ID.ID_http_server_port, color=gui_color.color_node_value);

            #dpg.configure_item(self.ID.ID_wallet, items=param_control.wallet_add)
        self.position_node()
        self.colorize_node()
    def position_node(self):
        data = parser_json.get_pos_from_json()
        dpg.set_item_pos(self.ID.ID_node, data["edge"]["hub"])
    def colorize_node(self):
        colorization.colorize_item(self.ID.ID_sock_server_l1_port, "node_value")
        colorization.colorize_item(self.ID.ID_sock_server_l2_port, "node_value")
        colorization.colorize_item(self.ID.ID_mqtt_client_name, "node_value")
        colorization.colorize_item(self.ID.ID_combo_lidar_source, "node_value")
        colorization.colorize_item(self.ID.ID_sock_client_l2_source, "node_value")
        colorization.colorize_node(self.ID.ID_node, "edge")

    # Update function
    def update(self):
        colorization.colorize_status(self.ID.ID_status_light, param_control.state_edge["hub"]["http"]["connected"])

    # Command function
    def command_false_alarm(self):
        print("[\033[1;32mOK\033[0m] Send false alarm")
        https_client_post.post_param_value("edge", None, "operator", "false_alarm")
    def command_port_socket(self):
        l1_port = dpg.get_value(self.ID.ID_sock_server_l1_port)
        l2_port = dpg.get_value(self.ID.ID_sock_server_l2_port)
        if(l1_port != l2_port):
            param_control.state_edge["hub"]["sock_server_l1_port"] = l1_port
            param_control.state_edge["hub"]["sock_server_l2_port"] = l2_port
            https_client_post.post_state("edge", param_control.state_edge)
    def command_mqtt(self):
        pass
        #param_control.state_cloud["operator"]["broker_port"] = dpg.get_value(object.object.operator.ID_mqtt_broker_port)
        #param_control.state_cloud["operator"]["mqtt_topic"] = dpg.get_value(object.object.operator.ID_mqtt_topic)
        #param_control.state_cloud["operator"]["mqtt_client"] = dpg.get_value(object.object.edge_1.ID_mqtt_client_name)
        #https_client_post.post_state("edge", param_control.state_edge)
        #https_client_post.post_param_value("edge", None, "operator", "reset")
    def command_combo_lidar_main(self):
        lidar_main = dpg.get_value(self.ID.ID_combo_lidar_source)
        https_client_post.post_param_value("edge", "self", "lidar_main", lidar_main)
        param_control.lidar_main = lidar_main
