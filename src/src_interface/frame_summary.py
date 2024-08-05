from tkinter import *
from src_road_graph.evrp_location_node import CustomerNode


class LocationNodeFrame(Frame):

    def __init__(self, master, node: tuple[CustomerNode, str]):
        super().__init__(master)
        self.master = master
        self.node: CustomerNode = node[0]
        self.label_txt: str = node[1]
        self.build_node()

    def build_node(self):

        self.lang_long_label = Label(self, text = f"{self.node.latitude:0.5f}, {self.node.longitude:0.5f}")
        self.lang_long_label.grid(row = 0, column = 0)

        self.label = Entry(self, width = 30)
        self.label.insert(END, self.label_txt)
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


        self.elements["Submit"] = Button(self, text = "Generate Dataset", command = lambda: self.master.run()).grid(row = 4, column = 0, pady = 10)