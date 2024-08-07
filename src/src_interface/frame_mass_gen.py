from tkinter import *

class InstanceNumberFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky="nsew")  # Ensure the frame fills its parent

        # Configure row and column weights to allow proper resizing
        self.grid_rowconfigure(0, weight=0)  # Row for the main label
        self.grid_rowconfigure(1, weight=0)  # Row for the description
        self.grid_rowconfigure(2, weight=1)  # Row for dropdown, scale/spinbox, and instances label
        self.grid_columnconfigure(0, weight=1)  # Column for labels and dropdown
        self.grid_columnconfigure(1, weight=1)  # Column for scale/spinbox
        self.grid_columnconfigure(2, weight=0)  # Column for instances label

        # Label for the number of instances
        self.lab_inst_num = Label(self, text="Number of Instances")
        self.lab_inst_num.grid(row=0, column=0, sticky='e', padx=5, pady=5)

        # Description label
        description = "This is the total number of EVRP routing problem instances to generate."
        self.lab_desc = Label(self, text=description)  # Wrap the text to avoid overflow
        self.lab_desc.grid(row=1, column=0, sticky='e', padx=5, pady=5, columnspan = 3)

        # Dropdown menu
        self.dropdown_var = StringVar(self)
        self.dropdown_var.set("Slider")  # Default value
        self.dropdown = OptionMenu(self, self.dropdown_var, "Slider", "Numerical", command=self.update_widget)
        self.dropdown.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        # Initialize widgets
        self.scale_inst_num = Scale(self, from_=1, to=150, orient=HORIZONTAL, length=300)
        self.spinbox_inst_num = Spinbox(self, from_=1, to=150, width=5)

        # Display the initial widget
        self.scale_inst_num.grid(row=2, column=1, padx=5, pady=5, sticky='e')
        self.spinbox_inst_num.grid_forget()  # Hide spinbox initially

        # Label for instances
        self.instances_label = Label(self, text="Instances")
        self.instances_label.grid(row=2, column=2, padx=5, pady=5, sticky='e')


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
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.remove = Button(self, text="X", command=lambda: controller.remove_location(self))
        self.remove.grid(row=0, column=1, padx=5, pady=5)



class CentralLocationsFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.lab_inst_num = Label(self, text="Central Locations")
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

        # Container to hold the location frames
        self.location_frame_container = Frame(self)
        self.location_frame_container.grid(row=2, column=0, columnspan=3, sticky="nsew")

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

    def remove_location(self, location: LocationNameFrame):
        if location in self.location_frames:
            location.grid_forget()  # Remove it from the layout
            self.location_frames.remove(location)
            location.destroy()  # Clean up the frame

            # Reposition remaining frames
            for index, frame in enumerate(self.location_frames):
                frame.grid(row=index, column=0, sticky="ew")

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

        self.min_customer_box.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.max_customer_box.grid(row = 0, column = 1, padx = 5, pady = 5)

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
            opts = ["Random", "Clustered", "Realistic", "Random & Clustered",
                    "Random & Realistic", "Realistic & Clustered", "Hybrid (All 3)"]

        Frame.__init__(self, master)
        self.grid()

        for i, o in enumerate(opts):
            l = Label(self, text=o)
            b = Spinbox(self, from_=0, to=100, width=3)
            al = Label(self, text="%")

            l.grid(row=0, column=i * 2, padx=2, pady=2, sticky=W, columnspan = 2)
            b.grid(row=1, column=i * 2, padx=(2, 0), pady=2, sticky=E)
            al.grid(row=1, column=i * 2 + 1, padx=(0, 2), pady=2, sticky=W)



class CustomerProportionFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="Customer Generation Configuration", font=("Arial bold", 16))
        self.cust_num.grid(row=0, column=0, sticky="w", padx= 5)

        self.cust_props = ProportionFrame(self)
        self.cust_props.grid(row = 1, column = 0, padx= 5)



class DepotProportionFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="Depot Generation Configuration", font=("Arial bold", 16))
        self.cust_num.grid(row=0, column=0, sticky="w", padx= 5)

        self.depot_props = ProportionFrame(self)
        self.depot_props.grid(row = 1, column = 0, padx= 5)



class EVChargePointProportionFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="EV Charge Point Generation Configuration", font=("Arial bold", 16))
        self.cust_num.grid(row=0, column=0, sticky="w", padx= 5)

        self.ev_props = ProportionFrame(self)
        self.ev_props.grid(row = 1, column = 0, padx= 5)



class TimeWindowTypeProportions(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="Time Window Type Proportions")
        self.cust_num.grid(row=0, column=0)

        self.tw_props = ProportionFrame(self, ["Narrow", "Moderate", "Wide"])
        self.tw_props.grid(row = 1, column = 0)



class TimeWindowMethodProportions(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="Time Window Method Proportions")
        self.cust_num.grid(row=0, column=0)

        self.tw_typ_props = ProportionFrame(self, ["Random", "Stratisfied"])
        self.tw_typ_props.grid(row = 1, column = 0)


class RangeFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.cust_num = Label(self, text="Node Count Configuration", font=("Arial bold", 16))
        self.cust_num.grid(row=0, column=0, sticky="w", padx=5, columnspan = 3)

        c = CustomerRangeFrame(self)
        c.grid(row=1, column=0, pady=10, sticky = "w")

        d = DepotRangeFrame(self)
        d.grid(row=1, column=1, pady=10, sticky = "nesw")

        e = EVChargeRangeFrame(self)
        e.grid(row=1, column=2, pady=10, sticky = "e")

if __name__ == "__main__":
    t = Tk()

    title = Label(t, text = "Mass Instance Specification Generator Tool")
    title.grid(row = 0, column = 0, padx = 5, pady = 5)

    f = InstanceNumberFrame(t)
    f.grid(row = 1, column = 0, pady = 10)

    f2 = CentralLocationsFrame(t)
    f2.grid(row = 2, column = 0, pady = 10)

    r = RangeFrame(t)
    r.grid(row = 3, column = 0, pady = 10, sticky = "w")

    pp = CustomerProportionFrame(t)
    pp.grid(row = 4, column = 0, pady = 10)

    dp = DepotProportionFrame(t)
    dp.grid(row = 5, column = 0, pady = 10)

    ep = EVChargePointProportionFrame(t)
    ep.grid(row = 6, column = 0, pady = 10)

    twp = TimeWindowTypeProportions(t)
    twp.grid(row = 7, column = 0, pady = 10)

    twm = TimeWindowMethodProportions(t)
    twm.grid(row = 7, column = 1, pady = 10)

    submit_button = Button(t, text="Submit", command=lambda:print("Done!"))
    submit_button.grid(row = 8, column = 0)

    t.mainloop()