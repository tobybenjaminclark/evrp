from tkinter import *
from src.src_road_graph.evrp_location_node import EVChargeNode

class EVNodeGUI:

    def __init__(self, parent, ev_node, name, manage_frame, _id, padx=0, moved=False):
        self.id = _id
        self.parent = parent
        self.name = name
        self.object = ev_node
        self.manage_frame = manage_frame
        self.bold_font = ("Arial bold", 10)
        self.font = ("Arial", 8)

        self.colour = "green"

        self.frame = self.create_ev()
        self.moved = moved
        self.icon = "🚚"
        


    def create_ev(self):
            
            self.container=  Frame(self.parent)
            self.container.pack(side=TOP, pady=10, padx=(20,0))



        
            latitude = round(self.object.latitude, 4)
            longitude = round(self.object.longitude, 4)
            ev_id = self.object.id
            
            charge_rate = self.object.charge_rate


            ev_frame = Frame(self.container, highlightbackground="black", highlightthickness=1)
            #ev_frame.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=2)


            contents_frame = Frame(ev_frame)
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

            lat_long_label = Label(info_frame, text=f"{latitude},{longitude}", font=self.font)
            lat_long_label.pack(anchor=W)

            check_frame=Frame(contents_frame)
            check_frame.pack(side=RIGHT)

            charge_rate_label=Label(check_frame,text=f"{charge_rate}kWh", font=self.font)
            charge_rate_label.pack(side=TOP)


            return ev_frame
    