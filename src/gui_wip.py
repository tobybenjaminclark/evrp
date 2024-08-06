from tkinter import *
from tkinter import ttk
import json
from src_apis.src_google_api import get_coordinates_from_keyword
from src_road_graph.find_locations import find_locations
from src_apis.src_open_heat_map import find_ev_charging_points


class EVRPInterface:

    def __init__(self, master):
        self.master = master
        self.master.attributes("-fullscreen", True)

        """ Master frame for toby """
        self.master_frame = Frame(self.master)
        self.master_frame.pack(fill=BOTH, expand=TRUE)

        self.init_gui()

        self.has_run = False

    def init_gui(self):
        # initialise the core gui elements

        self.list_frame = self.create_list_frame()

        # frame with tabs for customer, depot, ev charging points

        # frame to hold the tabs
        self.components_frame = Frame(self.master_frame)
        self.components_frame.pack(side=LEFT, fill=Y)

        self.tabs = ttk.Notebook(self.components_frame)

        self.customer_tab = self.create_customer_tab(self.tabs, self.list_frame)
        self.depot_tab = self.create_depot_tab(self.tabs, self.list_frame)
        self.ev_tab = self.create_ev_tab(self.tabs, self.list_frame)

        self.tabs.add(self.customer_tab, text="Customers")
        self.tabs.add(self.depot_tab, text="Depots")
        self.tabs.add(self.ev_tab, text="Charging Points")

        self.tabs.pack()

        # rhs has another frame listing chosen customers, tabs, evrps

    def create_list_frame(self):
        # Create the main frame
        list_frame = Frame(self.master_frame)
        list_frame.pack(side=RIGHT, fill=Y, expand=TRUE)

        # Create a Canvas widget
        canvas = Canvas(list_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # Create a Scrollbar widget
        scrollbar = Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create a Frame inside the Canvas
        content_frame = Frame(canvas)

        # Add the content_frame to the canvas
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Update the scroll region of the canvas
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Link the scrollbar to the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        generate_button = Button(content_frame, text="Generate", command=lambda: self.run())
        generate_button.pack(side=BOTTOM)

        return content_frame

    def run(self):

        print(f"selected customers: {self.selected_customers}")
        self.customers = [customer[3] for customer in self.selected_customers]
        self.depots = [depot[3] for depot in self.selected_depots]
        self.ev_chargers = [charger[3] for charger in self.ev_selected]

        for i1, node in enumerate(self.customers):
            node.id = "C" + str(i1)
        for i2, node in enumerate(self.depots):
            node.id = "C" + str(i2)
        for i3, node in enumerate(self.ev_chargers):
            node.id = "C" + str(i3)

        # set time slots
        time_slot_length = 60
        current_time = 0
        for index, node in enumerate(self.customers):
            if (current_time + time_slot_length) > 1440: current_time = 0
            node.time_slot = (current_time, current_time + time_slot_length)
            current_time += time_slot_length

        if (not self.has_run):
            self.has_run = True

            output_dict = {}
            d_custs = [
                {"latitude": l.latitude, "longitude": l.longitude, "demand": l.demand, "start_time": l.time_slot[0],
                 "end_time": l.time_slot[1]} for l in self.customers]
            d_depots = [{"latitude": l.latitude, "longitude": l.longitude} for l in self.depots]
            d_evs = [{"latitude": l.latitude, "longitude": l.longitude, "charge_rate": l.charge_rate} for l in
                     self.ev_chargers]
            d = {"customers": d_custs, "depots": d_depots, "chargers": d_evs, "output_path": "outputs/",
                 "instance_id": "geoff"}

            # Write to JSON file
            with open('test2.json', 'w') as file: json.dump(d, file, indent=4)

    def create_customer_tab(self, parent, list_tab):
        """ create a frame to hold customer information """
        self.customer_frame = Frame(parent)
        self.customer_frame.pack()

        self.selected_customers = []

        fields = {
            "Central Location": {
                "dropdown": ["Nottingham", "Preston", "Basildon"],
                "latlong": [],
                "text": []
            },
            "Keyword": {
                "dropdown": ["Costa", "McDonalds", "Sainsburys"],
                "text": []
            },

            "Radius": {
                "slider": [0, 200],
                "counter": [0, 200]
            }
        }

        self.create_subframes_to_create_and_manage(self.customer_frame, "Customers", fields, list_tab,
                                                   self.selected_customers)

        return self.customer_frame

    def create_depot_tab(self, parent, list_tab):
        """ create a frame to hold depot information """
        self.depot_frame = Frame(parent)
        self.depot_frame.pack()

        self.selected_depots = []

        fields = {
            "Central Location": {
                "dropdown": ["Nottingham", "Preston", "Basildon"],
                "latlong": [],
                "text": []
            },
            "Keyword": {
                "dropdown": ["Costa", "McDonalds", "Sainsburys"],
                "text": []
            },

            "Radius": {"slider": [0, 200],
                       "counter": [0, 200]
                       }
        }

        self.create_subframes_to_create_and_manage(self.depot_frame, "Depots", fields, list_tab, self.selected_depots)

        return self.depot_frame

    def create_ev_tab(self, parent, list_tab):
        """ create a frame to hold ev information """
        self.ev_frame = Frame(parent)
        self.ev_frame.pack()

        self.ev_selected = []

        fields = {
            "Central Location": {
                "dropdown": ["Nottingham", "Preston", "Basildon"],
                "latlong": [],
                "text": []
            },

            "Number": {"slider": [0, 200],
                       "counter": [0, 200]
                       }
        }

        self.create_subframes_to_create_and_manage(self.ev_frame, "Charging Points", fields, list_tab, self.ev_selected)

        return self.ev_frame

    def create_create_subframe(self, container_frame, item_managed: str, fields: dict[str, any], manage_frame):

        # Label for the item being managed
        create_label = Label(container_frame, text=f"Add {item_managed}")
        create_label.grid(row=0, column=0, columnspan=3, sticky=W + E)

        row = 1  # Start from the next row after the label

        for k, v in fields.items():
            # Label for the key of the field
            key_label = Label(container_frame, text=k)
            key_label.grid(row=row, column=0, sticky=W, padx=5, pady=2)

            # OptionMenu for choosing the type of field
            chosen_value_type = StringVar()
            default_value = next(iter(v))
            chosen_value_type.set(default_value)
            _options = list(v.keys())
            value_type = OptionMenu(container_frame, chosen_value_type, *_options)
            value_type.grid(row=row, column=1, sticky=W + E, padx=5, pady=2)

            # Frame for the specific type field (e.g., entry, dropdown)
            current_type_frame = Frame(container_frame)
            current_type_frame.grid(row=row, column=2, sticky=W + E, padx=5, pady=2)
            self.handle_changing_frame_type(default_value, current_type_frame, v)

            # Update the frame contents when the option changes
            chosen_value_type.trace_add("write", lambda var, x, y=chosen_value_type, frame=current_type_frame,
                                                        values=v: self.chosen_value_changed(var, frame, values))

            row += 1  # Move to the next row for the next field

        # Frame for the 'Add' button
        add_button_frame = Frame(container_frame)
        add_button_frame.grid(row=0, column=3, rowspan=row, sticky=N + S, pady=5)

        # 'Add' button itself
        add_button = Button(add_button_frame, text="➕",
                            command=lambda: self.add_request(item_managed, fields, manage_frame))
        add_button.grid(sticky=N + S + E + W)

        # Make sure the button expands to fill the entire cell
        add_button_frame.grid_rowconfigure(0, weight=1)
        add_button_frame.grid_columnconfigure(0, weight=1)
        container_frame.grid_rowconfigure(0, weight=1)
        for i in range(1, row):
            container_frame.grid_rowconfigure(i, weight=1)
        container_frame.grid_columnconfigure(3, weight=1)

        # Right-align the Add button
        container_frame.grid_columnconfigure(2, weight=1)  # Ensure the space before the button expands
        container_frame.grid_columnconfigure(3, weight=0)  # Button column does not expand

    def create_subframes_to_create_and_manage(self, parent, item_managed: str, fields: dict[str, any], list_tab,
                                              widget_list):

        # CREATE

        container_frame = Frame(parent)
        container_frame.pack(fill=BOTH, expand=TRUE)

        manage_frame = Frame(parent)
        manage_frame.pack(fill=BOTH, expand=TRUE, side=BOTTOM)

        list_frame = Frame(list_tab)
        list_frame.pack()

        list_header = Label(list_frame, text=f"Chosen {item_managed}")
        list_header.pack()

        contents_frame = self.create_manage_subframe(manage_frame, item_managed, list_frame, widget_list)

        self.create_create_subframe(container_frame, item_managed, fields, contents_frame)

    def select_all(self, widget_list):
        """ set every widget in the widget list to selected """
        for widget in widget_list:
            widget[1].set(True)

    def is_child(self, parent_frame, child_frame):
        current = child_frame
        while current:
            if current == parent_frame:
                return True
            current = current.master
        return False

    def move_selected_from_list(self, widget_list, new_parent_frame, old_parent_frame):
        """Move every selected widget to new_parent_frame."""

        index = 0

        for widget, is_selected, chosen, obj in widget_list:

            if chosen: continue

            # Check if the widget is selected
            if is_selected.get():
                widget.pack_forget()  # Detach the widget from its current layout manager

                duplicated_widget = self.clone_widget(widget, new_parent_frame)

                # Add widget to the new parent frame
                duplicated_widget.pack(fill=BOTH, expand=TRUE)

                is_selected.set(False)

                widget_list[index] = (duplicated_widget, is_selected, True, obj)

            index += 1

        # update scrollable region
        old_parent_frame.update_idletasks()

    def clone_widget(self, widget, master=None):
        """
        Create a cloned version o a widget

        Parameters
        ----------
        widget : tkinter widget
            tkinter widget that shall be cloned.
        master : tkinter widget, optional
            Master widget onto which cloned widget shall be placed. If None, same master of input widget will be used. The
            default is None.

        Returns
        -------
        cloned : tkinter widget
            Clone of input widget onto master widget.

        """
        # Get main info
        parent = master if master else widget.master
        cls = widget.__class__

        # Clone the widget configuration
        cfg = {key: widget.cget(key) for key in widget.configure()}
        cloned = cls(parent, **cfg)

        # Clone the widget's children
        for child in widget.winfo_children():
            child_cloned = self.clone_widget(child, master=cloned)
            if child.grid_info():
                grid_info = {k: v for k, v in child.grid_info().items() if k not in {'in'}}
                child_cloned.grid(**grid_info)
            elif child.place_info():
                place_info = {k: v for k, v in child.place_info().items() if k not in {'in'}}
                child_cloned.place(**place_info)
            else:
                pack_info = {k: v for k, v in child.pack_info().items() if k not in {'in'}}
                child_cloned.pack(**pack_info)

        return cloned

    def delete_selected(self, widget_list):
        """ remove every widget selected from the list """
        for widget in widget_list[:]:  # Use a slice of the list to avoid modifying it while iterating
            if widget[1].get() is True:
                # Remove it from the screen
                widget[0].pack_forget()
                # Remove it from the list
                widget_list.remove(widget)

    def create_manage_subframe(self, parent, item_managed, list_tab, widget_list):
        manage_label = Label(parent, text=f"Manage {item_managed}")
        manage_label.pack()

        # Create a frame to hold the scrollbar and canvas
        scroll_frame = Frame(parent)
        scroll_frame.pack(fill=BOTH, expand=TRUE)

        # Create a canvas widget
        canvas = Canvas(scroll_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # Create a vertical scrollbar linked to the canvas
        scrollbar = Scrollbar(scroll_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        master_frame = Frame(canvas)

        # Create a frame inside the canvas that will hold the buttons
        buttons_frame = Frame(master_frame)
        buttons_frame.pack()

        canvas.create_window((0, 0), window=master_frame, anchor='nw')

        # Configure the canvas and scrollbar
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))

        master_frame.bind('<Configure>', on_frame_configure)

        # Add buttons to the buttons_frame
        select_all_button = Button(buttons_frame, text="Select All", command=lambda: self.select_all(widget_list))
        select_all_button.pack(side=LEFT, fill=X, padx=5, pady=5)

        move_selected_button = Button(buttons_frame, text="Move Selected",
                                      command=lambda: self.move_selected_from_list(widget_list, list_tab, master_frame))
        move_selected_button.pack(side=LEFT, fill=X, padx=5, pady=5)

        delete_selected_button = Button(buttons_frame, text="Delete Selected",
                                        command=lambda: self.delete_selected(widget_list))
        delete_selected_button.pack(side=LEFT, fill=X, padx=5, pady=5)

        # Update canvas and scrollbar configuration
        canvas.configure(yscrollcommand=scrollbar.set)
        scroll_frame.update_idletasks()  # Update the scroll region

        contents_frame = Frame(master_frame)
        contents_frame.pack()

        return contents_frame

    def add_request(self, key, values, manage_frame):
        """ complete request to add customer/depot/ev charge """

        request_values = {}

        for k, v in values.items():
            if k == "Central Location":
                if v["type"] == "latlong":
                    request_values[k] = (v["value"][0].get(), v["value"][1].get())
                else:
                    request_values[k] = get_coordinates_from_keyword(v["value"].get())
            else:
                request_values[k] = v["value"].get()

        match key:
            case "Customers":
                rows = self.find_customers(request_values["Central Location"], request_values["Radius"],
                                           request_values["Keyword"])
                self.append_customers(manage_frame, rows)
            case "Depots":
                rows = self.find_depots(request_values["Central Location"], request_values["Radius"],
                                        request_values["Keyword"])
                self.append_depots(manage_frame, rows)
            case "Charging Points":
                rows = self.find_charging_points(request_values["Central Location"], request_values["Number"])
                self.append_ev(manage_frame, rows)
            case _:
                raise Exception(f"invalid key {key}")

    def append_customers(self, parent, list_of_customers):

        for customer in list_of_customers:
            name = customer[1]

            customer_obj = customer[0]
            latitude = customer_obj.latitude
            longitude = customer_obj.longitude
            demand = customer_obj.demand

            customer_frame = Frame(parent, highlightbackground="black", highlightthickness=1)
            customer_frame.pack(fill=X, expand=TRUE)

            info_frame = Frame(customer_frame)
            info_frame.pack(side=LEFT)

            name_label = Label(info_frame, text=name)
            name_label.pack(anchor=W)

            address_label = Label(info_frame, text="Address")
            address_label.pack(anchor=W)

            lat_long_label = Label(info_frame, text=f"{latitude},{longitude}")
            lat_long_label.pack(anchor=W)

            check_frame = Frame(customer_frame)
            check_frame.pack(side=RIGHT)

            rating_label = Label(check_frame, text=demand)
            rating_label.pack(anchor=E)

            is_checked = BooleanVar()

            check_box = Checkbutton(check_frame, variable=is_checked)
            check_box.pack(anchor=E)

            self.selected_customers.append((customer_frame, is_checked, False, customer_obj))

    def append_depots(self, parent, list_of_depots):

        for customer in list_of_depots:
            name = customer[1]

            depot_obj = customer[0]
            latitude = depot_obj.latitude
            longitude = depot_obj.longitude
            demand = depot_obj.demand

            depot_frame = Frame(parent, highlightbackground="black", highlightthickness=1)
            depot_frame.pack(fill=X, expand=TRUE)

            info_frame = Frame(depot_frame)
            info_frame.pack(side=LEFT)

            name_label = Label(info_frame, text=name)
            name_label.pack(anchor=W)

            address_label = Label(info_frame, text="Address")
            address_label.pack(anchor=W)

            lat_long_label = Label(info_frame, text=f"{latitude},{longitude}")
            lat_long_label.pack(anchor=W)

            check_frame = Frame(depot_frame)
            check_frame.pack(side=RIGHT)

            rating_label = Label(check_frame, text=demand)
            rating_label.pack(anchor=E)

            is_checked = BooleanVar()

            check_box = Checkbutton(check_frame, variable=is_checked)
            check_box.pack(anchor=E)

            self.selected_depots.append((depot_frame, is_checked, False, depot_obj))

    def append_ev(self, parent, list_of_evs):

        for customer in list_of_evs:
            ev_obj = customer[0]
            print(ev_obj)
            latitude = ev_obj.latitude
            longitude = ev_obj.longitude
            name = ev_obj.id

            charge_rate = ev_obj.charge_rate

            ev_frame = Frame(parent, highlightbackground="black", highlightthickness=1)
            ev_frame.pack(fill=X, expand=TRUE)

            info_frame = Frame(ev_frame)
            info_frame.pack(side=LEFT)

            name_label = Label(info_frame, text=name)
            name_label.pack(anchor=W)

            lat_long_label = Label(info_frame, text=f"{latitude},{longitude}")
            lat_long_label.pack(anchor=W)

            check_frame = Frame(ev_frame)
            check_frame.pack(side=RIGHT)

            charge_rate_label = Label(check_frame, text=charge_rate)
            charge_rate_label.pack(anchor=E)

            is_checked = BooleanVar()

            check_box = Checkbutton(check_frame, variable=is_checked)
            check_box.pack(anchor=E)

            self.ev_selected.append((ev_frame, is_checked, False, ev_obj))

    def find_customers(self, location, radius, keyword):
        locations = find_locations(location, radius, keyword)
        return locations

    def find_depots(self, location, radius, keyword):
        locations = find_locations(location, radius, keyword)
        return locations

    def find_charging_points(self, location, number):
        locations = find_ev_charging_points(*location, number)
        return locations

    def chosen_value_changed(self, changed_widget, frame, current_values):
        value = self.master.getvar(changed_widget)
        self.handle_changing_frame_type(value, frame, current_values)

    def handle_changing_frame_type(self, value, frame, current_values):
        """ change the type of a choice frame """

        for widget in frame.winfo_children():
            widget.destroy()

        match value:
            case "dropdown":
                val = self.replace_with_dropdown(frame, current_values["dropdown"])
                current_values["type"] = "dropdown"
            case "text":
                val = self.replace_with_text(frame, current_values["text"])
                current_values["type"] = "text"
            case "latlong":
                val = self.replace_with_latlong(frame, current_values["latlong"])
                current_values["type"] = "latlong"
            case "slider":
                val = self.replace_with_slider(frame, current_values["slider"])
                current_values["type"] = "slider"
            case "counter":
                val = self.replace_with_counter(frame, current_values["counter"])
                current_values["type"] = "counter"

        """ val is an array [lat,long] if lat long. otherwise val.get() """

        current_values["value"] = val

    def replace_with_dropdown(self, frame, options):

        # CREATE DROPDOWN
        option_selected = StringVar()

        # initial menu text
        option_selected.set(options[0])

        # Create Dropdown menu
        dropdown = OptionMenu(frame, option_selected, *options)
        dropdown.pack(side=LEFT)

        return option_selected

    def replace_with_text(self, frame, args):
        textbox_contents = StringVar()
        textbox = Entry(frame, textvariable=textbox_contents)
        textbox.pack(side=LEFT)

        return textbox_contents

    def replace_with_latlong(self, frame, args):

        lat_desc = Label(frame, text="Latitude:")
        lat_desc.pack(side=LEFT)

        lat_var = DoubleVar()
        lat_lbl = Entry(frame, textvariable=lat_var)
        lat_lbl.pack(side=LEFT)

        long_desc = Label(frame, text="Longitude:")
        long_desc.pack(side=LEFT)

        long_var = DoubleVar()
        long_lbl = Entry(frame, textvariable=long_var)
        long_lbl.pack(side=LEFT)

        return (lat_var, long_var)

    def replace_with_slider(self, frame, bounds):
        slider = Scale(frame, from_=bounds[0], to_=bounds[1], orient=HORIZONTAL)
        slider.pack(side=LEFT)

        return slider

    def replace_with_counter(self, frame, bounds):
        counter = Spinbox(frame, from_=bounds[0], to=bounds[1])
        counter.pack(side=LEFT)

        return counter


if __name__ == "__main__":
    root = Tk()
    gui = EVRPInterface(root)
    root.mainloop()