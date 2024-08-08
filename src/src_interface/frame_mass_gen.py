from tkinter import *
from tkinter import ttk


class InstanceNumberFrame(Frame):

    description = "This is the total number of instances to generate"

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky="nsew")  # Ensure the frame fills its parent

        # Configure row and column weights to allow proper resizing
        self.grid_rowconfigure(0, weight=0)  # Row for the main label
        self.grid_rowconfigure(1, weight=0)  # Row for the description
        self.grid_rowconfigure(2, weight=1)  # Row for dropdown, scale/spinbox, and instances label
        self.grid_rowconfigure(3, weight=1)  # Row for dropdown, scale/spinbox, and instances label
        self.grid_columnconfigure(0, weight=1)  # Column for labels and dropdown
        self.grid_columnconfigure(1, weight=1)  # Column for scale/spinbox
        self.grid_columnconfigure(2, weight=0)  # Column for instances label

        # Label for the number of instances
        self.lab_inst_num = Label(self, text="🚚 Number of Instances", font = ("Arial bold", 16))
        self.lab_inst_num.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.description = Label(self, text = self.description, font=("Arial", 12), wraplength = 1200, anchor = "w", justify = "left")
        self.description.grid(row = 1, column = 0, sticky="w", padx= 5, pady = (0, 10))

        # Dropdown menu
        self.dropdown_var = StringVar(self)
        self.dropdown_var.set("Slider")  # Default value
        self.dropdown = OptionMenu(self, self.dropdown_var, "Slider", "Numerical", command=self.update_widget)
        self.dropdown.config(width= 10)

        self.dropdown.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        # Initialize widgets
        self.scale_inst_num = Scale(self, from_=1, to=150, orient=HORIZONTAL, length=300)
        self.spinbox_inst_num = Spinbox(self, from_=1, to=150, width=5)

        # Display the initial widget
        self.scale_inst_num.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.spinbox_inst_num.grid_forget()  # Hide spinbox initially

        # Label for instances
        self.instances_label = Label(self, text="Instances")
        self.instances_label.grid(row=2, column=2, padx=5, pady=5, sticky='w')

    def update_widget(self, selection):
        if selection == "Slider":
            self.scale_inst_num.grid(row=2, column=1, padx=5, pady=5, sticky='w')
            self.spinbox_inst_num.grid_forget()
        elif selection == "Numerical":
            self.spinbox_inst_num.grid(row=2, column=1, padx=5, pady=5, sticky='w')
            self.scale_inst_num.grid_forget()



class LocationNameFrame(Frame):
    def __init__(self, master, text: str, controller: "CentralLocationsFrame"):
        Frame.__init__(self, master)
        self.grid()

        self.label = Label(self, text=text)
        self.label.grid(row=0, column=1, padx=5, pady=0)

        self.remove = Button(self, text="🗑️", command=lambda: controller.remove_location(self))
        self.remove.grid(row=0, column=0, padx=5, pady=0, ipady = 2)

class CentralLocationsFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.lab_inst_num = Label(self, text="🏙 Central Locations", font = ("Arial bold", 16))
        self.lab_inst_num.grid(row=0, column=0)

        # Shared variable to hold the value
        self.value_var = StringVar()

        # Dropdown to choose between 'Preset' and 'Custom'
        self.mode_var = StringVar(self)
        self.mode_var.set("Preset")  # Default value
        self.mode_dropdown = OptionMenu(self, self.mode_var, "Preset", "Custom", command=self.update_widget)
        self.mode_dropdown.grid(row=1, column=0)

        # Dropdown for city names
        self.city_var = StringVar(self)
        self.city_var.set("New York")  # Default city
        self.city_dropdown = OptionMenu(self, self.city_var, "New York", "Los Angeles", "Chicago", "Houston")
        self.city_dropdown.grid(row=1, column=1)

        # Entry widget for custom input
        self.custom_entry = Entry(self, textvariable=self.value_var)

        self.add_button = Button(self, text="+", command=self.add_location)
        self.add_button.grid(row=1, column=2)

        # Create a canvas for scrolling
        self.canvas = Canvas(self, height=150, width = 400)
        self.canvas.grid(row=2, column=0, columnspan=3, sticky="nsew")

        # Add a vertical scrollbar linked to the canvas
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=2, column=3, sticky="ns")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Create a frame to contain the location frames, and add it to the canvas
        self.location_frame_container = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.location_frame_container, anchor="nw")

        # Update scroll region to encompass the new location frames
        self.location_frame_container.bind("<Configure>", self.on_frame_configure)

        self.location_frames = []  # List to track location frames

        # Initially display the city names dropdown
        self.update_widget("Preset")

    def add_location(self):
        if self.mode_var.get() == "Preset":
            text = self.city_var.get()
        else:  # Custom
            text = self.value_var.get()

        if text:  # Only add if there's text
            location_frame = LocationNameFrame(self.location_frame_container, text, self)
            location_frame.grid(row=len(self.location_frames), column=0, sticky="ew")
            self.location_frames.append(location_frame)

            # Update scroll region after adding new frames
            self.update_scroll_region()

    def remove_location(self, location: LocationNameFrame):
        if location in self.location_frames:
            location.grid_forget()  # Remove it from the layout
            self.location_frames.remove(location)
            location.destroy()  # Clean up the frame

            # Reposition remaining frames
            for index, frame in enumerate(self.location_frames):
                frame.grid(row=index, column=0, sticky="ew")

            # Update scroll region after removing frames
            self.update_scroll_region()

    def update_widget(self, selection):
        if selection == "Preset":
            self.custom_entry.grid_forget()
            self.city_dropdown.grid(row=1, column=1, padx=5, pady=5)
            self.value_var.set(self.city_var.get())

        elif selection == "Custom":
            self.city_dropdown.grid_forget()
            self.custom_entry.grid(row=1, column=1, padx=5, pady=5)
            self.custom_entry.delete(0, END)
            self.custom_entry.insert(0, self.value_var.get())

    def on_frame_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_scroll_region(self):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


class InstanceRangeWidget(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="Minimum", font=("Arial", 12))
        self.cust_num.grid(row=1, column=0)

        self.cust_num = Label(self, text="Maximum", font=("Arial", 12))
        self.cust_num.grid(row=1, column=1)

        self.min_customer_box = Spinbox(self, from_=1, to=150, width=5)
        self.max_customer_box = Spinbox(self, from_=1, to=150, width=5)

        self.min_customer_box.grid(row = 0, column = 0, padx = 5, pady = 1)
        self.max_customer_box.grid(row = 0, column = 1, padx = 5, pady = 1)

class CustomerRangeFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="👤 Number of Customers", font=("Arial bold", 12))
        self.cust_num.grid(row=0, column=0)

        self.range_widget = InstanceRangeWidget(self)
        self.range_widget.grid(row = 1, column = 0)

class DepotRangeFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="🏢 Number of Depots", font=("Arial bold", 12))
        self.cust_num.grid(row=0, column=0)
        self.range_widget = InstanceRangeWidget(self)
        self.range_widget.grid(row = 1, column = 0)

class EVChargeRangeFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="⚡ Number of Chargers", font=("Arial bold", 12))
        self.cust_num.grid(row=0, column=0)
        self.range_widget = InstanceRangeWidget(self)
        self.range_widget.grid(row = 1, column = 0)


class ProportionFrame(Frame):
    def __init__(self, master, opts=None):
        if opts is None:
            opts = ["Random", "Clustered", "Realistic", "Rand. & Clust.",
                    "Rand. & Realistic", "Realistic & Clust.", "Hybrid"]

        Frame.__init__(self, master)
        self.grid()

        self.total_var = StringVar()
        self.total_var.set("0%")

        self.spinboxes = []

        for i, o in enumerate(opts):
            l = Label(self, text=o, font=("Arial", 10))
            b = Spinbox(self, from_=0, to=100, width=3, command=self.update_total)
            al = Label(self, text="%")

            l.grid(row=0, column=i * 2, padx=2, pady=2, sticky=W, columnspan=2)
            b.grid(row=1, column=i * 2, padx=(2, 0), pady=2, sticky=E)
            al.grid(row=1, column=i * 2 + 1, padx=(0, 2), pady=2, sticky=W)

            # Bind event to Spinbox
            b.bind("<KeyRelease>", lambda event: self.update_total())
            self.spinboxes.append(b)

        # Add total label
        self.total_txt = StringVar()
        self.total_txt.set("❌")

        total_label = Label(self, textvariable=self.total_txt)
        total_label.grid(row=0, column=len(opts) * 2, padx=(5, 0), pady=2, sticky=W)

        total_value_label = Label(self, textvariable=self.total_var)
        total_value_label.grid(row=1, column=len(opts) * 2, padx=(5, 0), pady=2, sticky=E)

    def update_total(self):
        total = 0
        for spinbox in self.spinboxes:
            total += int(spinbox.get())
        self.total_var.set(f"{total}%")
        if(total != 100.0):
            self.total_txt.set("❌")
        else:
            self.total_txt.set("✅")



class CustomerProportionFrame(Frame):

    description = "Customer nodes in an EVRP Instance can be generated randomly, in clusters or realistically -  or through any combination of these. The percentage assigned here refers to the percentage of problem instances that will be created using this generation technique to create customers - e.g. if you are generating 100 instances, and assign 50% to both random and clustered here, then the customers of 50 instances will be generated randomly, and the other 50 in a clustered manner. These values must sum to 100, shown on the right."

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="👤 Customer Generation Configuration", font=("Arial bold", 16))
        self.cust_num.grid(row=0, column=0, sticky="w", padx= 5)

        self.description = Label(self, text = self.description, font=("Arial", 12), wraplength = 1200, anchor = "w", justify = "left")
        self.description.grid(row = 1, column = 0, sticky="w", padx= 5, pady = (0, 10))

        self.cust_props = ProportionFrame(self)
        self.cust_props.grid(row = 2, column = 0, padx= 5)



class DepotProportionFrame(Frame):

    description = "Depot nodes in an EVRP Instance can be generated randomly, in clusters or realistically -  or through any combination of these. The percentage assigned here refers to the percentage of problem instances that will be created using this generation technique to create depots - e.g. if you are generating 100 instances, and assign 50% to both random and clustered here, then the depots of 50 instances will be generated randomly, and the other 50 in a clustered manner. These values must sum to 100, shown on the right."

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="🏢 Depot Generation Configuration", font=("Arial bold", 16))
        self.cust_num.grid(row=0, column=0, sticky="w", padx= 5)

        self.description = Label(self, text = self.description, font=("Arial", 12), wraplength = 1200, anchor = "w", justify = "left")
        self.description.grid(row = 1, column = 0, sticky="w", padx= 5, pady = (0, 10))

        self.depot_props = ProportionFrame(self)
        self.depot_props.grid(row = 2, column = 0, padx= 5)



class EVChargePointProportionFrame(Frame):

    description = "EV Charging Point nodes in an EVRP Instance can be generated randomly, in clusters or realistically -  or through any combination of these. The percentage assigned here refers to the percentage of problem instances that will be created using this generation technique to create EV Charging Points - e.g. if you are generating 100 instances, and assign 50% to both random and clustered here, then the charging points of 50 instances will be generated randomly, and the other 50 in a clustered manner. These values must sum to 100, shown on the right."

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="⚡ EV Charge Point Generation Configuration", font=("Arial bold", 16))
        self.cust_num.grid(row=0, column=0, sticky="w", padx= 5)

        self.description = Label(self, text = self.description, font=("Arial", 12), wraplength = 1200, anchor = "w", justify = "left")
        self.description.grid(row = 1, column = 0, sticky="w", padx= 5, pady = (0, 10))

        self.ev_props = ProportionFrame(self)
        self.ev_props.grid(row = 2, column = 0, padx= 5)



class TimeWindowTypeProportions(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="Time Window Type Proportions", font=("Arial bold", 14))
        self.cust_num.grid(row=0, column=0, sticky="w")

        self.tw_props = ProportionFrame(self, ["Narrow", "Moderate", "Wide"])
        self.tw_props.grid(row = 1, column = 0, sticky="w")



class TimeWindowMethodProportions(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="Time Window Method Proportions", font=("Arial bold", 14))
        self.cust_num.grid(row=0, column=0, sticky="w")

        self.tw_typ_props = ProportionFrame(self, ["Random", "Stratisfied"])
        self.tw_typ_props.grid(row = 1, column = 0, sticky="w")



class TimeWindowConfiguration(Frame):

    description = "Similar to the propotions defined above, here you can define what split of time window generation, as a percentage that should add to 100. Statisfied generation means the time windows are created methodically, and random means they are created randomly. You can also decide what percentage of instances should use narrow, moderate, and wide time windows respectively - note that this should also add to 100."

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="🕒 Time Window Generation Configuration", font=("Arial bold", 16))
        self.cust_num.grid(row=0, column=0, sticky="w", padx=5, columnspan=2)

        self.description = Label(self, text = self.description, font=("Arial", 12), wraplength = 1200, anchor = "w", justify = "left")
        self.description.grid(row = 1, column = 0, sticky="w", columnspan = 2, padx= 5, pady = (0, 10))

        self.method_frame = TimeWindowMethodProportions(self)
        self.method_frame.grid(row = 2, column = 0, sticky="w", padx = 25)

        self.type_frame = TimeWindowTypeProportions(self)
        self.type_frame.grid(row = 2, column = 1, sticky="w", padx = 25)



class RangeFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="⏺️ Node Count Configuration", font=("Arial bold", 16))
        self.cust_num.grid(row=0, column=0, sticky="w", padx=5, columnspan = 3)

        c = CustomerRangeFrame(self)
        c.grid(row=1, column=0, pady=10, sticky = "w")

        d = DepotRangeFrame(self)
        d.grid(row=1, column=1, pady=10, sticky = "nesw")

        e = EVChargeRangeFrame(self)
        e.grid(row=1, column=2, pady=10, sticky = "e")



class MassGeneratorFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        root = self

        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Instance Parameters")
        f = InstanceNumberFrame(tab1)
        f.grid(row = 0, column = 0, sticky = "w")

        f2 = CentralLocationsFrame(tab1)
        f2.grid(row = 1, column = 0, sticky = "w")

        r = RangeFrame(tab1)
        r.grid(row = 2, column = 0, sticky = "w")

        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Generation Settings")
        pp = CustomerProportionFrame(tab2)
        pp.grid(row = 0, column = 0, pady = 10)

        dp = DepotProportionFrame(tab2)
        dp.grid(row = 1, column = 0, pady = 10)

        ep = EVChargePointProportionFrame(tab2)
        ep.grid(row = 2, column = 0, pady = 10)

        twp = TimeWindowConfiguration(tab2)
        twp.grid(row = 3, column = 0, pady = 10)

        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Confirmation")

        submit_button = Button(tab3, text="Submit", command=lambda: print("Done!"))
        submit_button.pack(pady=10)

if __name__ == "__main__":
    root = Tk()
    root.geometry("1280x720")
    f = MassGeneratorFrame(root)
    f.grid(row = 0, column = 0, sticky = "NSEW")
    root.mainloop()