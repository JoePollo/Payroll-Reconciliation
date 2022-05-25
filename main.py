from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import pandas
from datetime import datetime

#----Constants---#
#--Constants are used due to global scope needed to store datasets for further analysis--#
#--Columns for datasets are kept as constant to allow for ease of manipulation in later occurrences, see rows 40-42--#
#--CONTRACT_CONTAINER is used to split output files based on each unique contract, rows 57-60--#
EMPLOYER_SUBMISSION_DATA_DATAFRAME = pandas.DataFrame()
RECORDKEEPING_DATA_DATAFRAME = pandas.DataFrame()
ACCOUNTING_DATA_DATAFRAME = pandas.DataFrame()
COMPARISON_COLUMNS = ["Contract", "Pay Period", "Effective Date", "Request Number",
                        "SSN", "Member ID", "Contribution ID", "Contribution Type", "Submission Amount"]
CONTRACTS_CONTAINER = []
#----Functions----#
#--Generate employer submission data--#
def employer_submission_data_file_upload():
    global EMPLOYER_SUBMISSION_DATA_DATAFRAME
    global CONTRACTS_CONTAINER
    try:
        employer_submission_data_file = askopenfilename(filetypes = [("Excel Files", "*.xlsx")])
        EMPLOYER_SUBMISSION_DATA_DATAFRAME = pandas.read_excel(employer_submission_data_file, usecols = COMPARISON_COLUMNS)
        CONTRACTS_CONTAINER = [
            contract for contract in EMPLOYER_SUBMISSION_DATA_DATAFRAME["Contract"] if contract not in CONTRACTS_CONTAINER
        ]
    except ValueError:
        messagebox.showerror(title = "Oops!", message = "Please check the file used is correct.")
    else:
        messagebox.showinfo(title = "Uploaded!", message = "Employer submission file uploaded.")
        employer_submission_button.config(text = "Submission data uploaded.")
#--Generate transactional recordkeeping data--#
def recordkeeping_data_file_upload():
    global RECORDKEEPING_DATA_DATAFRAME
    global COMPARISON_COLUMNS
    global CONTRACTS_CONTAINER
    try:
        recordkeeping_data_file = askopenfilename(filetype = [("Excel Files", "*.xlsx")])
        #--Change [Submission Amount] to [Transaction Amount] in accordance with verbage change in queries--#
        del COMPARISON_COLUMNS[8]
        COMPARISON_COLUMNS += ["Transaction Amount"]
        RECORDKEEPING_DATA_DATAFRAME = pandas.read_excel(recordkeeping_data_file, usecols = COMPARISON_COLUMNS)
        for contract in RECORDKEEPING_DATA_DATAFRAME["Contract"]:
            if contract not in CONTRACTS_CONTAINER:
                CONTRACTS_CONTAINER.append(contract)
    except ValueError:
        messagebox.showerror(title = "Oops!", message = "Please check the file used is correct.")
    else:
        messagebox.showinfo(title = "Uploaded!", message = "Recordkeeping file uploaded.")
        recordkeeping_button.config(text = "Recordkeeping data uploaded.")
#--Generate accounting data by contract--#
def accounting_data_file_upload():
    global COMPARISON_COLUMNS
    global ACCOUNTING_DATA_DATAFRAME
    try:
        accounting_data_file = askopenfilename(filetypes = [("Excel Files", "*.xlsx")])
        #--Remove [Pay Period, Transaction Amount, Requset Number, Contribution ID, Contribution Type] from COMPARISON_COLUMNS--#
        #--Columns are not present in Accounting Query--#
        delete_columns = [1,7,2,4,4]
        for column in delete_columns:
            del COMPARISON_COLUMNS[column]
        COMPARISON_COLUMNS += ["Transaction Category", "Cash Amount"]
        ACCOUNTING_DATA_DATAFRAME = pandas.read_excel(accounting_data_file, usecols = COMPARISON_COLUMNS)
        ACCOUNTING_DATA_DATAFRAME = ACCOUNTING_DATA_DATAFRAME["Transaction Category" ==  "MOF"]
    except ValueError:
        messagebox.showerror(title = "Oops!", message = "Please check the file used is correct.")
    else:
        messagebox.showinfo(title = "Uploaded!", message = "Accounting file uploaded.")
        accounting_button.config(text = "Accounting data uploaded.")
#--Compare employer submission and transactional recordkeeping data--#
def compare():
    global CONTRACTS_CONTAINER
    comparison_df = EMPLOYER_SUBMISSION_DATA_DATAFRAME.merge(RECORDKEEPING_DATA_DATAFRAME, how = "outer")
    comparison_df = comparison_df.merge(ACCOUNTING_DATA_DATAFRAME, how = "outer")
                                        # , on = ["Contract", "SSN", "Member ID", "Effective Date"])
    comparison_df = comparison_df.fillna(0)
    comparison_df["Submission vs Recordkeeping"] = comparison_df["Submission Amount"] - comparison_df["Transaction Amount"]
    for contract in CONTRACTS_CONTAINER:
        contract_df = comparison_df[comparison_df["Contract"] == contract]
        date_time = datetime.now().strftime("%m_%d_%y-%I-%M-%S-%p")
        contract_df.to_excel(f"Contract {contract} Payroll Reconciliation {date_time}.xlsx", index = False)
#--Clears data sets stored in constants--#
def reset():
    global EMPLOYER_SUBMISSION_DATA_DATAFRAME
    global RECORDKEEPING_DATA_DATAFRAME
    global COMPARISON_COLUMNS
    global CONTRACTS_CONTAINER
    EMPLOYER_SUBMISSION_DATA_DATAFRAME = pandas.DataFrame()
    RECORDKEEPING_DATA_DATAFRAME = pandas.DataFrame()
    COMPARISON_COLUMNS = ["Contract", "Pay Period", "Effective Date", "Request Number",
                        "SSN", "Member ID", "Contribution ID", "Contribution Type", "Submission Amount"]
    employer_submission_button.config(text = "Upload Employer Submission Spreadsheet")
    recordkeeping_button.config(text = "Upload Recordkeeping Spreadsheet")
    CONTRACTS_CONTAINER = []
#----Application Window Management----#
mainapp = Tk()
mainapp.geometry("600x300")
mainapp.title("Payroll Reconciliation")
employer_submission_button = Button(text = "Upload Employer Submission Spreadsheet", command = employer_submission_data_file_upload)
employer_submission_button.pack()
recordkeeping_button = Button(text = "Upload Recordkeeping Spreadsheet", command = recordkeeping_data_file_upload)
recordkeeping_button.pack()
compare_button = Button(text = "Compare Spreadsheets", command = compare)
compare_button.pack()
accounting_button = Button(text = "Upload Accounting Spreadsheet", command = accounting_data_file_upload)
accounting_button.pack()
reset_button = Button(text = "Restart", command = reset)
reset_button.pack()
mainapp.mainloop()
