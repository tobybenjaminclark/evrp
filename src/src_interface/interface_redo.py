from tkinter import *
from tkinter import ttk, filedialog
import json
from src.src_apis.src_google_api import get_coordinates_from_keyword
from src.src_road_graph.find_locations import find_locations
from src.src_apis.src_open_heat_map import find_ev_charging_points

from src.src_interface.customer_node_gui import CustomerNodeGUI
from src.src_interface.depot_node_gui import DepotNodeGUI
from src.src_interface.ev_node_gui import EVNodeGUI

import os



class EVRPInterface:

    def __init__(self, master):
        self.master = master

        self.master_frame = Frame(self.master)
        self.master_frame.pack(fill=BOTH, expand=TRUE)

        self.init_gui()

    def init_gui(self):

        self.list_frame = self.create_list_frame()

        # frame with tabs for customer, depot, ev charging points

        # frame to hold the tabs
        self.components_frame = Frame(self.master_frame, width=640)

        canvas = Canvas(self.components_frame, width=640,height=1,bg="blue")
        canvas.pack(fill=X)
        
        self.components_frame.pack(side=LEFT, fill=BOTH)
        self.tabs = ttk.Notebook(self.components_frame)

        self.customer_tab = self.create_customer_tab(self.tabs, self.list_frame)
        self.depot_tab = self.create_depot_tab(self.tabs, self.list_frame)
        self.ev_tab = self.create_ev_tab(self.tabs, self.list_frame)
        

        self.tabs.add(self.customer_tab, text="Customers")
        self.tabs.add(self.depot_tab, text="Depots")
        self.tabs.add(self.ev_tab, text="Charging Points")

        self.tabs.pack(side=TOP, fill=BOTH,expand=TRUE)

    
    def create_params_frame(self, parent):
        params_frame = Frame(parent)
        params_frame.pack(fill=X)

        height_canvas = Canvas(params_frame, height=175, bg="pink", width=1)
        height_canvas.pack(side=RIGHT)

        # CREATE A CONTENTS FRAME TO NOT MESS WITH SET HEIGHT

        content_frame = Frame(params_frame)
        content_frame.pack(fill=BOTH, expand=TRUE)

        top_frame = Frame(content_frame)
        top_frame.pack(side=TOP, fill=BOTH, expand=TRUE)

        time_window_frame = Frame(top_frame)
        time_window_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)

        time_window_label = Label(time_window_frame, text="Time Window")
        time_window_label.pack()

        self.time_window_option = StringVar()
        wide_button = Radiobutton(time_window_frame, text="Wide", value="wide", var=self.time_window_option)
        wide_button.pack()
        moderate_button = Radiobutton(time_window_frame, text="Moderate", value="moderate", var=self.time_window_option)
        moderate_button.pack()
        narrow_button = Radiobutton(time_window_frame, text="Narrow", value="narrow", var=self.time_window_option)
        narrow_button.pack()


        window_gen_frame = Frame(top_frame)
        window_gen_frame.pack(side=RIGHT, fill=BOTH, expand=TRUE)

        window_gen_label = Label(window_gen_frame, text="Window Gen")
        window_gen_label.pack()

        self.window_gen_option = StringVar()
        random_button = Radiobutton(window_gen_frame, text="Random", value="random", var=self.window_gen_option)
        random_button.pack()
        moderate_button = Radiobutton(window_gen_frame, text="Stratisfied", value="stratisfied", var=self.window_gen_option)
        moderate_button.pack()


        bottom_frame=Frame(content_frame)
        bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=TRUE)

        vehicle_frame = Frame(bottom_frame)
        vehicle_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)

        vehicle_label = Label(vehicle_frame, text="Vehicle")
        vehicle_label.pack(side=LEFT)

        self.chosen_vehicle = StringVar()
        vehicles = ["Vehicle1", "Vehicle2", "Vehicle3"]
        vehicle_dropdown = OptionMenu(vehicle_frame, self.chosen_vehicle, vehicles)
        vehicle_dropdown.pack(side=LEFT)
        self.chosen_vehicle.set(vehicles[0])

        open_button = Button(vehicle_frame, text="Open File", command=self.open_file_dialog)
        open_button.pack(side=LEFT)

        generate_frame = Frame(bottom_frame)
        generate_frame.pack(side=RIGHT, fill=BOTH, expand=TRUE)

        # Create a Generate button
        generate_button = Button(generate_frame, text="Generate", command=lambda: self.run())
        generate_button.pack(side=RIGHT)

        return params_frame


    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("JSON file", "*.json"), ("All files", "*.*")])
        if file_path:
            #process_file(file_path)
            file_name = os.path.basename(file_path)
            self.chosen_vehicle.set(file_name)
        
    def create_list_frame(self):

        master_frame = Frame(self.master_frame)
        master_frame.pack(side=RIGHT, fill=Y)

        canvas=Canvas(master_frame, width=640,height=1,bg="red")
        canvas.pack(fill=X)

        params_frame = self.create_params_frame(master_frame)

        # Create the main frame
        list_frame = Frame(master_frame)
        list_frame.pack(fill=BOTH, expand=TRUE) 

        self.create_buttons(list_frame, BOTTOM, 4)

        # Create a Canvas widget
        canvas = Canvas(list_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Create a Scrollbar widget
        scrollbar = Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create a Frame inside the Canvas
        content_frame = Frame(canvas)
        content_frame.pack(fill=BOTH, expand=TRUE)

        # Add the content_frame to the canvas
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Update the scroll region of the canvas
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Link the scrollbar to the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        return content_frame

    
    def run(self):

        # item[2] = item is in the generate frame
        self.customers = [customer.object for customer in self.selected_customers if customer.moved]
        self.depots = [depot.object for depot in self.selected_depots if depot.moved]
        self.ev_chargers = [charger.object for charger in self.ev_selected if charger.moved]

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


        output_dict = {}
        d_custs = [{"latitude": l.latitude, "longitude": l.longitude, "demand": l.demand, "start_time":l.time_slot[0], "end_time":l.time_slot[1] } for l in self.customers]
        d_depots = [{"latitude": l.latitude, "longitude": l.longitude } for l in self.depots]
        d_evs = [{"latitude": l.latitude, "longitude": l.longitude, "charge_rate": l.charge_rate} for l in self.ev_chargers]
        d = {"customers": d_custs, "depots": d_depots, "chargers": d_evs, "output_path": "outputs/", "instance_id": "geoff"}

        # Write to JSON file
        with open('../../../../../Downloads/evrp 2/test2.json', 'w') as file: json.dump(d, file, indent=4)

        
    def create_customer_tab(self, parent, list_tab):
        """ create a frame to hold customer information """
        self.customer_frame = Frame(parent)
        
        self.customer_frame.pack(fill=BOTH,expand=TRUE)

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
                       "slider":[0, 2000],
                       "counter": [0,2000]
                      }
        }


        self.create_subframes_to_create_and_manage(self.customer_frame, "Customers", fields, list_tab, self.selected_customers)


        return self.customer_frame
    
    
    def create_depot_tab(self, parent, list_tab):
        """ create a frame to hold depot information """
        self.depot_frame = Frame(parent)
        self.depot_frame.pack(fill=BOTH, expand=TRUE)

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
                            
            "Radius": {"slider":[0, 2000],
                       "counter": [0,2000]
                      }
        }

        self.create_subframes_to_create_and_manage(self.depot_frame, "Depots", fields, list_tab, self.selected_depots)


        
        return self.depot_frame


    def create_ev_tab(self, parent, list_tab):
        """ create a frame to hold ev information """
        self.ev_frame = Frame(parent)
        self.ev_frame.pack(fill=BOTH, expand=TRUE)

        self.ev_selected = []

        fields = {
            "Central Location": {
                                 "dropdown": ["Nottingham", "Preston", "Basildon"],
                                 "latlong": [],
                                 "text": []
                                 },
                            
            "Number": {"slider":[0, 200],
                       "counter": [0,200]
                      }
        }


        self.create_subframes_to_create_and_manage(self.ev_frame, "Charging Points", fields, list_tab, self.ev_selected)

        return self.ev_frame
    
    def create_create_subframe(self, container_frame, parent, item_managed: str, fields:dict[str, any], manage_frame, list_frame):


        # Label for the item being managed
        create_label = Label(container_frame, text=f"Add {item_managed}")
        create_label.grid(row=0, column=0, columnspan=3, sticky=W+E)

        row = 1  # Start from the next row after the label

        for k, v in fields.items():
            # Label for the key of the field
            key_label = Label(container_frame, text=k)
            key_label.grid(row=row, column=0, sticky=W, padx=2)

            # OptionMenu for choosing the type of field
            chosen_value_type = StringVar()
            default_value = next(iter(v))
            chosen_value_type.set(default_value)
            _options = list(v.keys())
            value_type = OptionMenu(container_frame, chosen_value_type, *_options)
            value_type.grid(row=row, column=1, sticky=W+E, padx=2)

            # Frame for the specific type field (e.g., entry, dropdown)
            current_type_frame = Frame(container_frame)
            current_type_frame.grid(row=row, column=2, sticky=W+E, padx=2)
            self.handle_changing_frame_type(default_value, current_type_frame, v)

            # Update the frame contents when the option changes
            chosen_value_type.trace_add("write", lambda var, x, y=chosen_value_type, frame=current_type_frame, values=v: self.chosen_value_changed(var, frame, values))

            row += 1  # Move to the next row for the next field

        # Make sure the button expands to fill the entire cell
        """add_button_frame.grid_rowconfigure(0, weight=1)
        add_button_frame.grid_columnconfigure(0, weight=1)
        container_frame.grid_columnconfigure(3, weight=1)

        # Right-align the Add button
        container_frame.grid_columnconfigure(2, weight=1)  # Ensure the space before the button expands
        container_frame.grid_columnconfigure(3, weight=0)  # Button column does not expand"""



    
    def create_subframes_to_create_and_manage(self, parent, item_managed: str, fields: dict[str, any], list_tab, widget_list):

        
        # CREATE

        create_frame = Frame(parent)
        create_frame.pack(side=TOP,fill=X)
        

        canvas = Canvas(create_frame, height=125,width=1,bg="yellow")
        canvas.pack(side=RIGHT)

        # Frame for the 'Add' button
        add_button_frame = Frame(create_frame,bg="red")
        add_button_frame.pack(fill=Y, side=RIGHT)



        container_frame = Frame(create_frame)
        container_frame.pack(fill=BOTH,expand=TRUE)


        manage_frame = Frame(parent)
        manage_frame.pack(fill=BOTH, expand=TRUE)

        list_frame = Frame(list_tab)
        list_frame.pack()

        list_header = Label(list_frame, text=f"Chosen {item_managed}")
        list_header.pack(fill=BOTH, expand=TRUE)

        self.create_buttons(manage_frame, BOTTOM, 0, widget_list)

        contents_frame = self.create_manage_subframe(manage_frame, item_managed, widget_list)

        # 'Add' button itself
        add_button = Button(add_button_frame, text="➕", command=lambda: self.add_request(item_managed, fields, contents_frame, list_frame))
        add_button.pack(fill=BOTH,expand=TRUE)

        self.create_create_subframe(container_frame, create_frame, item_managed, fields, contents_frame, list_frame)

        
        
    def select_all(self, widget_list=None, moved=False):
        """ set every widget in the widget list to selected """

        # if there is no widget list, run the command for every list
        if widget_list is None:
            self.select_all(widget_list=self.selected_customers, moved=True)
            self.select_all(widget_list=self.selected_depots, moved=True)
            self.select_all(widget_list=self.ev_selected, moved=True)

        for widget in widget_list:
            if widget is None: continue 

            if widget.moved == moved:
                widget.is_checked=True
                widget.check_box.config(text="☑️")

    def is_child(self, parent_frame, child_frame):
        current = child_frame
        while current:
            if current == parent_frame:
                return True
            current = current.master
        return False

    def move_selected_from_list(self, widget_list=None, moved=False):
        """Move every selected widget to new_parent_frame."""

        # if there is no widget list, run the command for every list
        if widget_list is None:
            self.move_selected_from_list(widget_list=self.selected_customers, moved=True)
            self.move_selected_from_list(widget_list=self.selected_depots, moved=True)
            self.move_selected_from_list(widget_list=self.ev_selected, moved=True)

        for widget in widget_list:

            if widget is None: continue

            if widget.is_checked and widget.moved == moved:
                self.move(widget, widget_list)


    def move(self, widget, widget_list):
            # Check if the widget is selected

                index = widget_list.index(widget)
            
                widget.container.pack_forget()  # Detach the widget from its current layout manager

                # create a new widget with the same details 

                if widget.moved:
                    
                    widget_list[index] = self.create_item(widget.manage_frame, type(widget), widget.object, widget.name, widget_list, widget.parent, widget.id, moved=False)
                else:
                    widget_list[index] = self.create_item(widget.manage_frame, type(widget), widget.object, widget.name, widget_list, widget.parent, widget.id, moved=True)
                
                widget.parent.update_idletasks()
                widget.manage_frame.update_idletasks()


            
    def delete_selected(self, widget_list=None, moved=False):

        # if there is no widget list, run the command for every list
        if widget_list is None:
            self.delete_selected(widget_list=self.selected_customers, moved=True)
            self.delete_selected(widget_list=self.selected_depots, moved=True)
            self.delete_selected(widget_list=self.ev_selected, moved=True)

        """ remove every widget selected from the list """
        for widget in widget_list[:]:  # Use a slice of the list to avoid modifying it while iterating
            if widget is None: continue
            if widget.is_checked and widget.moved == moved:
                self.delete(widget, widget_list)


    def delete(self, widget, widget_list):
        # Remove it from the screen
        widget.container.pack_forget()
        # Remove it from the list, make it none to retain IDs
        widget_list[widget_list.index(widget)] = None



    def create_manage_subframe(self, parent, item_managed, widget_list):
        #manage_label = Label(parent, text=f"Manage {item_managed}")
        #manage_label.pack()

        # Create a frame to hold the scrollbar and canvas
        scroll_frame = Frame(parent)
        scroll_frame.pack(fill=BOTH, expand=TRUE)

        # Create a canvas widget
        canvas = Canvas(scroll_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # Create a vertical scrollbar linked to the canvas
        scrollbar = Scrollbar(scroll_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create a frame inside the canvas that will hold the widgets
        master_frame = Frame(canvas)
        
        # Add the frame to the canvas
        canvas.create_window((0, 0), window=master_frame, anchor=NW)

        # Configure the canvas and scrollbar
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
            # Ensure the frame is correctly positioned and resized
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        master_frame.bind('<Configure>', on_frame_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        #master_frame.pack(fill=X, expand=TRUE)

        return master_frame


    def create_buttons(self, parent, side, pady, widget_list=None):
        # Add buttons below the canvas
        buttons_frame = Frame(parent)
        buttons_frame.pack(fill=X, side=side, pady=pady)

        select_all_button = Button(buttons_frame, text="Select All", command=lambda: self.select_all(widget_list))
        select_all_button.pack(side=LEFT, padx=5, fill=X, expand=TRUE)

        move_selected_button = Button(buttons_frame, text="Move Selected", command=lambda: self.move_selected_from_list(widget_list))
        move_selected_button.pack(side=LEFT, padx=5, fill=X, expand=TRUE)

        delete_selected_button = Button(buttons_frame, text="Delete Selected", command=lambda: self.delete_selected(widget_list))
        delete_selected_button.pack(side=LEFT, padx=5, fill=X, expand=TRUE)




    def add_request(self, key, values, manage_frame, list_frame):
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
                rows = self.find_customers(request_values["Central Location"], request_values["Radius"], request_values["Keyword"])
                self.append_item(manage_frame, rows, CustomerNodeGUI, self.selected_customers, list_frame)
            case "Depots":
                rows = self.find_depots(request_values["Central Location"], request_values["Radius"], request_values["Keyword"])
                print(f"depot: {rows}")
                self.append_item(manage_frame, rows, DepotNodeGUI, self.selected_depots, list_frame)
            case "Charging Points":
                rows = self.find_charging_points(request_values["Central Location"], request_values["Number"])
                print(f"charging point: {rows}")
                self.append_item(manage_frame, rows, EVNodeGUI, self.ev_selected, list_frame)
            case _:
                raise Exception(f"invalid key {key}")
            

        
    def append_item(self, parent, list_of_items, object_class, item_list, list_frame):

        
        for item_tuple in list_of_items:
            _id = len(item_list)
            item = self.create_item(parent, object_class, *item_tuple, item_list, list_frame, _id)
            item_list.append(item)

        # update scrollable region
        parent.update_idletasks()
        list_frame.update_idletasks()

    def create_item(self, parent, object_class, obj, name, item_list, list_frame, _id, moved=False):


        item = object_class(parent, obj, name, list_frame, _id, moved=moved)
        
        icon_frame = Frame(item.container, width=5)
        icon_frame.pack(side=LEFT, fill=Y)

        icon_button = Button(icon_frame, text=f"{item.id}\n\n{item.icon}", width=5)
        icon_button.pack(fill=Y, expand=TRUE)

        item.frame.pack(side=LEFT, fill=BOTH, expand=TRUE)

        buttons_frame = Frame(item.container)
        buttons_frame.pack(side=LEFT, fill=Y)

        delete_button = Button(buttons_frame, text='❌', command=lambda: self.delete(item, item_list), width=4)
        delete_button.pack()

        move_icon = '⬅️' if item.moved else '➡️'
        move_button = Button(buttons_frame, text=move_icon, command=lambda: self.move(item, item_list), width=4)
        move_button.pack()

        is_checked = False

        item.check_box = Button(buttons_frame, text='☐', command=lambda i=item: self.toggle_check(i), width=4)
        item.check_box.pack()

        item.is_checked = is_checked

        return item



    def toggle_check(self, item):
        if item.is_checked:
            item.check_box.config(text='☐', width = 4)
            item.is_checked=False
        else:
            item.check_box.config(text='☑️', width = 4)
            item.is_checked=True

        

    
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