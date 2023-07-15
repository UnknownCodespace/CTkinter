from tkinter import *
import tkinter as tk
import customtkinter as ctk

'''

PROGRAM LOGIC / PARAM

Check to see previous HDL
Check to see current HDl
Check to see previous history of C.V.D

If yes previous C.V.D:
    Check to see if current is lower than 2.5#
    if yes then maintain
    else advise to see doctor

If no:
    make sure current value is less than 60% of previous value
    if not flag

'''

class Base(ctk.CTk):

    def __init__(self):

        '''

        Create initial CTk window
        Create base frame for other frames to be built on

        '''

        ctk.set_appearance_mode("Dark")

        # Save base values in controller rather than frame so can be accessed between other frames

        self.CVD_Threshold = 2.5
        self.CVD_Percentage = 40

        ctk.CTk.__init__(self)

        self.selected_font = "Bahnschrift"

        self.title_font = ctk.CTkFont(family = self.selected_font, size = 16)

        self.custom_font = ctk.CTkFont(family = self.selected_font, size = 12)

        self.title("HDL Calculator")

        self.resizable(False, False)

        container = ctk.CTkFrame(self, width = 400, height = 400)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        # Initiate other frames

        for F in (Settings, Calculator):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(Calculator)

    def show_frame(self, window):

        # Switch current frame based on dictionary as saved frame

        frame = self.frames[window]
        frame.tkraise()


class Calculator(ctk.CTkFrame):

    def __init__(self, parent, controller):

        '''
        :param parent:
        :param controller:

        Create calulator frame using Base class as parent
        Add frame to current frame stack

        '''

        ctk.CTkFrame.__init__(self, parent)

        self.History_Value = StringVar()

        self.grid_rowconfigure(5, minsize = 50)
        self.grid_rowconfigure(2, minsize = 50)

        Calculator_L = ctk.CTkLabel(self, text = "Calculator", font = controller.title_font)
        HDL_C_L = ctk.CTkLabel(self, text = "Current HDL", font = controller.custom_font)
        HDL_P_L = ctk.CTkLabel(self, text = "Previous HDL", font = controller.custom_font)
        History_L = ctk.CTkLabel(self, text = "History of CVD", font = controller.custom_font)
        self.Output_Message = ctk.CTkLabel(self, text = "", font = controller.custom_font)

        self.HDL_C_T = ctk.CTkEntry(self)
        self.HDL_P_T = ctk.CTkEntry(self)
        self.History_T = ctk.CTkOptionMenu(self, values = ("Yes", "No"), variable = self.History_Value, font = controller.custom_font)
        Calculate_B = ctk.CTkButton(self, text = "Calculate", command = lambda: self.calculate_result(controller), font = controller.custom_font)
        Setting_B = ctk.CTkButton(self, text = "Settings", command = lambda: controller.show_frame(Settings), font = controller.custom_font)

        Calculator_L.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)

        HDL_C_L.grid(row = 1, column = 0, padx = 5, pady = 5)
        HDL_P_L.grid(row = 2, column = 0, padx = 5, pady = 5)
        History_L.grid(row = 3, column = 0, padx = 5, pady = 5)

        self.HDL_C_T.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.HDL_P_T.grid(row = 2, column = 1, padx = 5, pady = 5)
        self.History_T.grid(row = 3, column = 1, padx = 5, pady = 5)

        self.Output_Message.grid(row = 4, column = 0, columnspan = 2 , padx = 5, pady = 5)
        Setting_B.grid(row=5, column = 0, padx = 5, pady = 5)
        Calculate_B.grid(row = 5, column = 1, padx = 5, pady = 5)

    def validate_input(self):

        if self.HDL_C_T.get() == "":
            self.Output_Message.configure(text = "No current HDL level")
            return

        if self.HDL_P_T.get() == "":
            self.Output_Message.configure(text = "No previous HDL level")
            return

        try:
            float(self.HDL_C_T.get())

        except ValueError:
            self.Output_Message.configure(text = "Current HDL value error")
            return

        try:
            float(self.HDL_P_T.get())

        except ValueError:
            self.Output_Message.configure(text = "Previous HDL value error")
            return

        if self.History_Value.get() == "":
            self.Output_Message.configure(text = "No history selected")
            return

        return True

    def calculate_result(self, controller):

        if not self.validate_input():
            return

        if self.History_Value.get() == "Yes":

            if float(self.HDL_C_T.get()) <= float(controller.CVD_Threshold):
                self.Output_Message.configure(text = "Maintain current managment")
                return

            self.Output_Message.configure(text = "Speak to doctor")
            return

        if self.History_Value.get() == "No":

            percentage_change = int(((float(float(self.HDL_C_T.get())) - float(self.HDL_P_T.get())) / float(self.HDL_C_T.get())) * 100)

            if percentage_change == 0:
                self.Output_Message.configure(text = "No change")
                return

            if percentage_change <= float(controller.CVD_Percentage):
                self.Output_Message.configure(text = "Review current managment")
                return

            else:
                self.Output_Message.configure(text=f'Change {percentage_change}% decrease, maintian current management')
                return


            self.Output_Message.configure(text = f'Change {percentage_change}% increase, speak to doctor')
            return

        # Should never run

        self.Output_Message.configure(text = "Error calculating value")



class Settings(ctk.CTkFrame):

    def __init__(self, parent, controller):

        '''
        :param parent:
        :param controller:

        Create settings frame using Base class as parent
        Add frame to current frame stack

        '''

        ctk.CTkFrame.__init__(self, parent)

        self.grid_rowconfigure(4, minsize=50)
        self.grid_columnconfigure(1, minsize=50)

        Settings_L = ctk.CTkLabel(self, text = "Settings",font = controller.title_font)
        Threshold_L = ctk.CTkLabel(self, text = "HDL Threshold",font = controller.custom_font)
        Percentage_L = ctk.CTkLabel(self, text = "Percentage Threshold",font = controller.custom_font)
        self.Output_Message = ctk.CTkLabel(self, text = "",font = controller.custom_font)

        self.Threshold_T = ctk.CTkEntry(self)
        self.Percentage_T = ctk.CTkEntry(self)
        self.wipe_and_reset_fields(controller)

        Back_B = ctk.CTkButton(self, text = "Back", command = lambda: self.exit(controller))
        Save_B = ctk.CTkButton(self, text = "Save", command = lambda: self.save(controller))

        Settings_L.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
        Threshold_L.grid(row = 1, column = 0, padx = 5, pady = 5)
        Percentage_L.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.Threshold_T.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.Percentage_T.grid(row = 2, column = 1, padx = 5, pady = 5)
        self.Output_Message.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 5)

        Back_B.grid(row = 4, column = 0, padx = 5, pady = 5)
        Save_B.grid(row = 4, column = 1, padx = 5, pady = 5)

    def wipe_and_reset_fields(self, controller):

        # Reset fields to saved controller value

        self.Threshold_T.delete(0, END)
        self.Percentage_T.delete(0, END)

        self.Threshold_T.insert(0, controller.CVD_Threshold)
        self.Percentage_T.insert(0, controller.CVD_Percentage)

    def exit(self, controller):

        # Reset fields without saving user input

        self.Output_Message.configure(text = "")

        self.wipe_and_reset_fields(controller)

        controller.show_frame(Calculator)

    def save(self, controller):

        # Validate then save user settings (Dosen't quit back to calculator frame)

        if not self.validate_input():
            return

        controller.CVD_Threshold = self.Threshold_T.get()
        controller.CVD_Percentage = self.Percentage_T.get()

        self.Output_Message.configure(text = "Saved settings")

        return True


    def validate_input(self):

        try:
            float(self.Threshold_T.get())

        except ValueError:
            self.Output_Message.configure(text = "Threshold error")
            return

        try:
            int(self.Percentage_T.get())
            if int(self.Percentage_T.get()) > 100:
                self.Output_Message.configure(text = "Percentage out of range")
                return

        except ValueError:
            self.Output_Message.configure(text = "Percentage error")
            return

        return True