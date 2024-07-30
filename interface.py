from tkinter import *
from frame_start import LocationFrame
from frame_depots import DepotFrame
from frame_summary import SummaryFrame
from src_road_graph.evrp_location_node import LocationNode
from frame_evs import EVFrame
from src_road_graph.find_locations import create_customer_graph2
from PIL import Image, ImageTk
import csv



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
        self.locations: list[LocationNode] = []
        self.has_run = False
        self.depots: list[LocationNode] = []
        self.ev_chargers: list[LocationNode] = []

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
            node.set_id("C", i1)
        for i2, node in enumerate(self.depots):
            node.set_id("D", i2)
        for i3, node in enumerate(self.ev_chargers):
            node.set_id("E", i3)

        # set time slots
        time_slot_length = 60
        current_time = 0
        for index, node in enumerate(self.locations):
            if (current_time + time_slot_length) > 1440: current_time = 0

            node.time_slot = (current_time, current_time + time_slot_length)
            current_time += time_slot_length

        nodes = self.locations + self.ev_chargers + self.depots

        if (not self.has_run):
            self.has_run = True
            x = create_customer_graph2(self.locations, self.depots, self.ev_chargers)

            # Initialize matrices
            node_ids = [node.id for node in nodes]

            # Create an initial matrix with infinite values, except for the diagonal
            matrix = {node_id: {nid: 0 if nid == node_id else float('inf') for nid in node_ids} for node_id in node_ids}
            time_matrix = {node_id: {nid: 0 if nid == node_id else float('inf') for nid in node_ids} for node_id in
                           node_ids}

            # Populate matrices with energy consumption and time taken
            for node in nodes:
                for dest_id, energy, time_taken in node.journeys:
                    matrix[node.id][dest_id] = energy
                    time_matrix[node.id][dest_id] = time_taken

            # Initialize the location matrix with demand values
            location_matrix = {node.id: {'demand': 0, 'start_of_slot': 0, 'end_of_slot': 0} for node in self.locations}
            for cnode in self.locations:
                location_matrix[cnode.id]['demand'] = cnode.demand
                location_matrix[cnode.id]['start_of_slot'] = cnode.time_slot[0]
                location_matrix[cnode.id]['end_of_slot'] = cnode.time_slot[1]

            # Write to CSV
            with open('node_journeys.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Write customer demands
                writer.writerow(['Customer Demand'])
                writer.writerow(['Node ID', 'Demand', 'Start of Time Slot', 'End of Time Slot'])
                for node_id in location_matrix.keys():
                    writer.writerow([node_id, location_matrix[node_id]['demand'], location_matrix[node_id]['start_of_slot'], location_matrix[node_id]['end_of_slot']])

                # Write EC matrix header
                writer.writerow([])  # Empty line for separation
                writer.writerow(['EC Matrix'])
                writer.writerow([''] + node_ids)  # Header row
                for node_id in node_ids:
                    row = [node_id] + [matrix[node_id][nid] for nid in node_ids]
                    writer.writerow(row)

                # Write time matrix header
                writer.writerow([])  # Empty line for separation
                writer.writerow(['Time Matrix'])
                writer.writerow([''] + node_ids)  # Header row
                for node_id in node_ids:
                    row = [node_id] + [time_matrix[node_id][nid] for nid in node_ids]
                    writer.writerow(row)


    def mainloop(self):
        while True:
            self.update()


# Create and run the application
app = Window()
