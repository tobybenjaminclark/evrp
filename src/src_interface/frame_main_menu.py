from tkinter import *
from src.src_interface.frame_mass_gen import *
from src.src_interface.interface_redo import *

class MainMenuFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.grid()

        self.mass_gen_button = Button(text = "Generate EVRP Problem Instance Specification", width = 50)
        self.mass_gen_button.grid(row = 0, column = 0)

        self.mass_gen_button = Button(text = "Generate Instance Specifications (Multiple)", width = 50, command = lambda: self.master.switch_frame(MassGeneratorFrame))
        self.mass_gen_button.grid(row = 1, column = 0)

        self.mass_gen_button = Button(text = "Run Instance Specification", width = 50)
        self.mass_gen_button.grid(row = 2, column = 0)

class Program(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("1280x720")

        self.current_frame = MainMenuFrame(self)
        self.current_frame.grid(row = 0, column = 0)

        self.mainloop()

    def switch_frame(self, frame):
        self.current_frame.grid_forget()
        self.current_frame = frame(self)
        self.current_frame.grid(row = 0, column = 0)