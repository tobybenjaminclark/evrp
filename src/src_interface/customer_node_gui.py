from tkinter import *
from src.src_road_graph.evrp_location_node import CustomerNode

class CustomerNodeGUI:

    def __init__(self, parent, customer_node, name, manage_frame, id, padx=0, moved=False):
        # each customer has a customernode and an associated frame
        self.id = id
        self.parent = parent
        self.name = name
        self.object = customer_node
        self.icon = "👤"
        self.bold_font = ("Arial bold", 10)
        self.font = ("Arial", 8)

        self.manage_frame = manage_frame

        self.star_icon = PhotoImage(file="../../../../../Downloads/evrp 2/assets/star.png")

        self.colour="red"

        self.frame = self.create_customer(padx)
        self.moved = moved

    def create_customer(self, padx):
        """ given a customer node, create a frame """

        self.container=  Frame(self.parent)
        self.container.pack(side=TOP, fill=X, pady=10, padx=(20,0))

        latitude = round(self.object.latitude, 4)
        longitude = round(self.object.longitude, 4)
        demand = self.object.demand

        customer_frame = Frame(self.container, highlightbackground="black", highlightthickness=1, width=500)
        #customer_frame.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=2)

        contents_frame = Frame(customer_frame)
        contents_frame.pack()

            
        canvas = Canvas(contents_frame, width=475,height=2, bg=self.colour)
        canvas.pack(side=TOP)

        info_frame = Frame(contents_frame)
        info_frame.pack(side=LEFT)

        name_frame = Frame(info_frame)
        name_frame.pack()

        name_label = Label(name_frame, text=self.name)
        name_label.pack(side=LEFT)
        name_label.config(font=self.bold_font)

        address_label = Label(info_frame, text="Address", font=self.font)
        address_label.pack(anchor=W)

        lat_long_label = Label(info_frame, text=f"{latitude},{longitude}", font=self.font)
        lat_long_label.pack(anchor=W)

        

        check_frame=Frame(contents_frame)
        check_frame.pack(side=RIGHT)

        rating_frame = Frame(check_frame)
        rating_frame.pack(side=TOP)

        rating_label=Label(rating_frame,text=f"{demand}", font=self.font)
        rating_label.pack(side=LEFT)

        star_label = Label(rating_frame, image=self.star_icon)
        star_label.pack(side=LEFT)

        return customer_frame
    
    