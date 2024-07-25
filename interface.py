from tkinter import *
from frame_start import LocationFrame
from frame_depots import DepotFrame
from frame_summary import SummaryFrame
from src_road_graph.evrp_location_node import LocationNode
from frame_evs import EVFrame
from src_road_graph.find_locations import create_customer_graph2
from PIL import Image, ImageTk




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
            node.set_id("c", i1)
        for i2, node in enumerate(self.depots):
            node.set_id("d", i2)
        for i3, node in enumerate(self.ev_chargers):
            node.set_id("e", i3)

        if (not self.has_run):
            self.has_run = True
            x = create_customer_graph2(self.locations, self.depots, self.ev_chargers)




    def mainloop(self):
        while True:
            self.update()


# Create and run the application
app = Window()
