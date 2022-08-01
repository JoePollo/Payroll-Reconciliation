from tkinter import Tk, Button, Label, Frame, messagebox
from tkinter.font import BOLD

COLOR_DICTIONARY = {
    "BACKGROUND": "#0076CF",
    "BUTTON_SUCCESS": "#00A29B",
    "BUTTON_NEUTRAL": "#F76800",
    "ERROR": "#C00000",
    "TEXT": "#333333"
}

class Interface:
    def __init__(self):
        ###---------MAINAPP---------###
        self.mainapp = Tk()
        self.mainapp.geometry("600x300")
        self.mainapp.title("Payroll Reconciliation")
        self.mainapp.configure(background = COLOR_DICTIONARY["BACKGROUND"])
        
        
        ###---------EMPLOYER SUBMISSION UI---------###
        self.employerSubmissionButtonBorder = Frame(self.mainapp,
                                                    highlightbackground = COLOR_DICTIONARY["TEXT"],
                                                    highlightthickness = 2,
                                                    bd = 0)
        self.employerSubmissionButton = Button(self.employerSubmissionButtonBorder,
                                               text = "Upload",
                                               bg = COLOR_DICTIONARY["BUTTON_NEUTRAL"],
                                               fg = COLOR_DICTIONARY["TEXT"])
        self.employerSubmissionLabel = Label(text = "Employer Submission Spreadsheet: ",
                                             font = ("FS Elliot Pro", 10, BOLD),
                                             fg = COLOR_DICTIONARY["TEXT"],
                                             bg = COLOR_DICTIONARY["BACKGROUND"])
        
        
        ###---------RECORDKEEPING UI---------###
        self.recordkeepingButtonBorder = Frame(self.mainapp,
                                                    highlightbackground = COLOR_DICTIONARY["TEXT"],
                                                    highlightthickness = 2,
                                                    bd = 0)
        self.recordkeepingButton = Button(self.recordkeepingButtonBorder,
                                          text = "Upload",
                                          bg = COLOR_DICTIONARY["BUTTON_NEUTRAL"],
                                          fg = COLOR_DICTIONARY["TEXT"])
        self.recordkeepingLabel = Label(text = "Recordkeeping Spreadsheet: ",
                                        font = ("FS Elliot Pro", 10, BOLD),
                                        fg = COLOR_DICTIONARY["TEXT"],
                                        bg = COLOR_DICTIONARY["BACKGROUND"])
        
        
        ###---------ACCOUNTING UI---------###
        self.accountingButtonBorder = Frame(self.mainapp,
                                                    highlightbackground = COLOR_DICTIONARY["TEXT"],
                                                    highlightthickness = 2,
                                                    bd = 0)
        self.accountingButton = Button(self.accountingButtonBorder,
                                          text = "Upload",
                                          bg = COLOR_DICTIONARY["BUTTON_NEUTRAL"],
                                          fg = COLOR_DICTIONARY["TEXT"])
        self.accountingLabel = Label(text = "Accounting Spreadsheet: ",
                                        font = ("FS Elliot Pro", 10, BOLD),
                                        fg = COLOR_DICTIONARY["TEXT"],
                                        bg = COLOR_DICTIONARY["BACKGROUND"])
        
        
        ###---------GEOMETRY MANAGER---------###
        self.employerSubmissionLabel.grid(row = 0,
                                          column = 0)
        self.employerSubmissionButtonBorder.grid(row = 0,
                                           column = 1)
        self.employerSubmissionButton.grid(row = 0,
                                           column = 1)
        self.recordkeepingLabel.grid(row = 1,
                                     column = 0)
        self.recordkeepingButtonBorder.grid(row = 1,
                                            column = 1)
        self.recordkeepingButton.grid(row = 1,
                                      column = 1)
        self.accountingLabel.grid(row = 2,
                                     column = 0)
        self.accountingButtonBorder.grid(row = 2,
                                            column = 1)
        self.accountingButton.grid(row = 2,
                                      column = 1)

        self.mainapp.mainloop()