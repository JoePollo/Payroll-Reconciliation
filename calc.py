from pandas import DataFrame, read_excel, ExcelWriter, merge
from tkinter.filedialog import askopenfilename

class Payroll_Calculator:
    def __init__(self):
        self.employerSubmissionDF: DataFrame
        self.recordkeepingDF: DataFrame
        self.accountingDF: DataFrame
        self.ui = Interface()
        
        def employerSubmissionUpload(self) -> DataFrame: 
            self.employerSubmissionDF = read_excel(askopenfilename(filetypes = [("Excel Files","*.xlsx")])
                                                   )