from tkinter import *
from src.src_interface.frame_mass_gen import *
from src.src_interface.interface_redo import *

class MainMenuFrame(Frame):
    def __init__(self, master, parent):
        Frame.__init__(self, master)
        self.parent = parent
        self.master = master
        self.grid()

        self.mass_gen_button = Button(self, text = "Generate EVRP Problem Instance Specification", width = 50, command = lambda: self.parent.switch_frame(EVRPInterface))
        self.mass_gen_button.grid(row = 0, column = 0)

        self.mass_gen_button = Button(self, text = "Generate Instance Specifications (Multiple)", width = 50, command = lambda: self.parent.switch_frame(MassGeneratorFrame))
        self.mass_gen_button.grid(row = 1, column = 0)

        self.mass_gen_button = Button(self, text = "Run Instance Specification", width = 50)
        self.mass_gen_button.grid(row = 2, column = 0)

class Program(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("1300x720")

        self.internal_frame = Frame(self)
        self.internal_frame.pack(fill=BOTH, expand=TRUE)

        self.current_frame = MainMenuFrame(self.internal_frame, self)
        self.current_frame.pack(fill=BOTH, expand=TRUE)

        self.mainloop()

    def switch_frame(self, frame):
        self.current_frame.pack_forget()
        self.internal_frame.pack_forget()

        self.internal_frame = Frame(self)

        self.current_frame = frame(self.internal_frame)
        if(frame is not EVRPInterface): self.current_frame.pack(fill=BOTH, expand=TRUE)

        self.internal_frame.pack(fill=BOTH, expand=TRUE)