#---------------------------------------------
from src.gui.background import gui_ID
import dearpygui.dearpygui as dpg


class Block_edge:
    def __init__(self, ID):
        self.ID = ID

    def design_block(self):
        with dpg.node(label="Edge", tag=self.ID.ID_block_edge):
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_image(self.ID.ID_icon_edge, width=35, height=30)
                dpg.add_text("")
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                with dpg.drawlist(width=350, height=350):
                    pass

    def set_visibility(self, what):
        if(what == False):
            dpg.hide_item(self.ID.ID_block_edge)
        elif(what == True):
            dpg.show_item(self.ID.ID_block_edge)
