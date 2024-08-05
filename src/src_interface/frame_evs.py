from tkinter import *
from src_road_graph.evrp_location_node import  CustomerNode, EVChargeNode
from src_apis.src_open_heat_map import find_ev_charging_points

from src_apis.src_google_api import get_coordinates_from_keyword

class LocationNodeFrame(Frame):

    def __init__(self, master, node: tuple[EVChargeNode, str]):
        super().__init__(master)
        self.master = master
        self.node: CustomerNode = node[0]
        self.node_txt: str = node[1]
        self.build_node()

    def build_node(self):

        self.lang_long_label = Label(self, text = f"{self.node.latitude:0.5f}, {self.node.longitude:0.5f}")
        self.lang_long_label.grid(row = 0, column = 0)

        self.label = Entry(self, width = 30)
        self.label.insert(END, self.node_txt)
        self.label.grid(row = 0, column = 1, padx = 10)

        self.destroy_button = Button(self, text = "Remove")
        self.destroy_button.grid(row = 0, column = 2)




class EVFrame(Frame):
    NUMBER_OF_TEXT_FIELDS = 4  # Define the number of text fields

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.elements = {}
        self.locnodes = []
        self.configure_elements()

    def add_locations(self):

        origin = self.elements["Entry1"].get()
        radius = self.elements["Entry3"].get()

        locations = find_ev_charging_points(*get_coordinates_from_keyword(origin), radius)
        newlocnodes = [LocationNodeFrame(self, node) for node in locations]
        self.locnodes.extend(newlocnodes)
        self.redraw()

    def redraw(self):
        # Remove existing
        for n in self.locnodes:
            try: n.grid_forget()
            except: pass

        try: self.submit_customers_button.grid_forget()
        except: pass

        # Correctly reference the new nodes in locnodes
        for i, n in enumerate(self.locnodes):
            n.destroy_button.config(command=lambda n=n: self.remove_location(n))
            n.grid(row=8 + i, column=0)

        # Add in Customer Info (total)
        self.submit_customers_button = Button(self, text = f"Proceed with {len(self.locnodes)} EV Charging Points", command = lambda: self.submit_customers())
        self.submit_customers_button.grid(row = 8 + i + 1, column = 0)

    def remove_location(self, n: CustomerNode):
        self.locnodes.remove(n)
        n.grid_forget()
        self.redraw()

    def submit_customers(self):
        self.master.ev_chargers = [n.node for n in self.locnodes]
        self.master.next_frame()


    def configure_elements(self):


        self.elements["Label1"] = Label(self, text = "EV Charging Point Finder\n\nPlease enter a Origin Location, i.e. Nottingham")
        self.elements["Entry1"] = Entry(self)

        self.elements["Label3"] = Label(self, text = "Please enter a number to to add")
        self.elements["Entry3"] = Entry(self)

        self.elements["Label1"].grid(row = 1, column = 0)
        self.elements["Entry1"].grid(row = 2, column = 0)
        self.elements["Label3"].grid(row = 5, column = 0)
        self.elements["Entry3"].grid(row = 6, column = 0)


        self.elements["Submit"] = Button(self, text = "Search for Depots", command = lambda: self.add_locations()).grid(row = 7, column = 0, pady = 10)