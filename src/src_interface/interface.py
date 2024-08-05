from tkinter import *
from frame_start import LocationFrame
from frame_depots import DepotFrame
from frame_summary import SummaryFrame
from src_road_graph.evrp_location_node import CustomerNode, DepotNode, EVChargeNode
from frame_evs import EVFrame
from PIL import Image, ImageTk
import csv
import json


class GeneralFrame2(Frame):
    NUMBER_OF_TEXT_FIELDS = 4  # Define the number of text fields

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.elements = {}
        self.configure_elements()

    def configure_elements(self):

        txt = "\n".join([str(n) for n in self.master.locations])
        self.elements["Label1"] = Label(self, text = txt).grid(row = 0, column = 0)
        self.elements["Entry1"] = Entry(self).grid(row = 1, column = 0)
        self.elements["Submit"] = Button(self, text = "Submit", command = lambda: self.master.next_frame()).grid(row = 2, column = 0)


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x900")
        self.minsize(900, 900)
        self.locations: list[CustomerNode] = []
        self.has_run = False
        self.depots: list[DepotNode] = []
        self.ev_chargers: list[EVChargeNode] = []

        # Load the PNG image
        image_path = "EVRPLogo.png"
        image = Image.open(image_path)
        self.logo = ImageTk.PhotoImage(image)

        self.photo = Label(self, image = self.logo).grid(row = 0, column = 1)
        for i in range(0, 3): self.columnconfigure(i, weight = 1)

        # Configure the window layout
        self.configure_layout()

        # Start the main loop
        self.mainloop()

    def next_frame(self):
        self.frame1.grid_forget()

        if isinstance(self.frame1, LocationFrame): self.frame1 = DepotFrame(self)
        elif isinstance(self.frame1, DepotFrame): self.frame1 = EVFrame(self)
        elif isinstance(self.frame1, EVFrame): self.frame1 = SummaryFrame(self)

        self.frame1.grid(row = 1, column = 1)

    def configure_layout(self):
        # Create four frames, one for each quarter of the window
        self.frame1 = LocationFrame(self)
        self.frame1.grid(row = 1, column = 1)

    def run(self):

        for i1, node in enumerate(self.locations):
            node.id = "C" + str(i1)
        for i2, node in enumerate(self.depots):
            node.id = "C" + str(i2)
        for i3, node in enumerate(self.ev_chargers):
            node.id = "C" + str(i3)

        # set time slots
        time_slot_length = 60
        current_time = 0
        for index, node in enumerate(self.locations):
            if (current_time + time_slot_length) > 1440: current_time = 0
            node.time_slot = (current_time, current_time + time_slot_length)
            current_time += time_slot_length

        if (not self.has_run):
            self.has_run = True

            output_dict = {}
            d_custs = [{"latitude": l.latitude, "longitude": l.longitude, "demand": l.demand, "start_time":l.time_slot[0], "end_time":l.time_slot[1] } for l in self.locations]
            d_depots = [{"latitude": l.latitude, "longitude": l.longitude } for l in self.depots]
            d_evs = [{"latitude": l.latitude, "longitude": l.longitude, "charge_rate": l.charge_rate} for l in self.ev_chargers]
            d = {"customers": d_custs, "depots": d_depots, "chargers": d_evs, "output_path": "outputs/", "instance_id": "geoff"}

            # Write to JSON file
            with open('../test2.json', 'w') as file: json.dump(d, file, indent=4)

    def mainloop(self):
        while True:
            self.update()


# Create and run the application
app = Window()
