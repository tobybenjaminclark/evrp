from tkinter import *
from PIL import ImageTk, Image
from src_road_graph.find_locations import find_locations
from src_road_graph.evrp_location_node import LocationNode
from src_open_heat_map import find_ev_charging_points

from src_google_api import get_coordinates_from_keyword

class LocationNodeFrame(Frame):

    def __init__(self, master, node: LocationNode):
        super().__init__(master)
        self.master = master
        self.node: LocationNode = node
        self.build_node()

    def build_node(self):

        self.lang_long_label = Label(self, text = f"{self.node.latitude:0.5f}, {self.node.longitude:0.5f}")
        self.lang_long_label.grid(row = 0, column = 0)

        self.label = Entry(self, width = 30)
        self.label.insert(END, self.node.label)
        self.label.grid(row = 0, column = 1, padx = 10)

        self.destroy_button = Button(self, text = "Remove")
        self.destroy_button.grid(row = 0, column = 2)




class SummaryFrame(Frame):
    NUMBER_OF_TEXT_FIELDS = 4  # Define the number of text fields

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.elements = {}
        self.locnodes = []
        self.configure_elements()

    def submit_customers(self):
        self.master.ev_chargers = [n.node for n in self.locnodes]
        self.master.next_frame()


    def configure_elements(self):


        self.elements["Label1"] = Label(self, text = "Summary")
        self.elements["Label1"].grid(row = 0, column = 0)

        d = self.master.depots
        ev = self.master.ev_chargers
        l = self.master.locations

        self.elements["Label2"] = Label(self, text = "Depots:\n\n" + "\n".join([str(d1) for d1 in d]))
        self.elements["Label2"].grid(row = 1, column = 0, pady = 10)

        self.elements["Label2"] = Label(self, text = "Charging Points:\n\n" + "\n".join([str(ev1) for ev1 in ev]))
        self.elements["Label2"].grid(row = 2, column = 0, pady = 10)

        self.elements["Label3"] = Label(self, text = "Customers:\n\n" + "\n".join([str(l2) for l2 in l]))
        self.elements["Label3"].grid(row = 3, column = 0, pady = 10)


        self.elements["Submit"] = Button(self, text = "Generate Dataset", command = lambda: print("A")).grid(row = 4, column = 0, pady = 10)