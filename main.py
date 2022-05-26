from tkinter import *
import tkinter
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import pandas
from datetime import datetime
from os import getcwd, path, makedirs

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
CURRENT_DIRECTORY = getcwd()
FILE_NAME_CONTAINER = []
#----Functions----#
#--Generate employer submission data--#
def employer_submission_data_file_upload():
    global EMPLOYER_SUBMISSION_DATA_DATAFRAME
    global CONTRACTS_CONTAINER
    try:
        employer_submission_data_file = askopenfilename(filetypes = [("Excel Files", "*.xlsx")])
        employer_submission_file_name.config(text = employer_submission_data_file)
        EMPLOYER_SUBMISSION_DATA_DATAFRAME = pandas.read_excel(employer_submission_data_file, usecols = COMPARISON_COLUMNS)
        CONTRACTS_CONTAINER = [
            contract for contract in EMPLOYER_SUBMISSION_DATA_DATAFRAME["Contract"] if contract not in CONTRACTS_CONTAINER
        ]
    except ValueError:
        messagebox.showerror(title = "Oops!", message = "Please check the file used is correct.")
    else:
        messagebox.showinfo(title = "Uploaded!", message = "Employer submission file uploaded.")
#--Generate transactional recordkeeping data--#
def recordkeeping_data_file_upload():
    global RECORDKEEPING_DATA_DATAFRAME
    global COMPARISON_COLUMNS
    global CONTRACTS_CONTAINER
    try:
        recordkeeping_data_file = askopenfilename(filetype = [("Excel Files", "*.xlsx")])
        recordkeeping_file_name.config(text = recordkeeping_data_file)
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
#--Generate accounting data by contract--#
def accounting_data_file_upload():
    global COMPARISON_COLUMNS
    global ACCOUNTING_DATA_DATAFRAME
    try:
        accounting_data_file = askopenfilename(filetypes = [("Excel Files", "*.xlsx")])
        accounting_file_name.config(text = accounting_data_file)
        #--Remove [Pay Period, Transaction Amount, Requset Number, Contribution ID, Contribution Type] from COMPARISON_COLUMNS--#
        #--Columns are not present in Accounting Query--#
        delete_columns = [1,7,2,4,4]
        for column in delete_columns:
            del COMPARISON_COLUMNS[column]
        COMPARISON_COLUMNS += ["Transaction Category", "Cash Amount"]
        ACCOUNTING_DATA_DATAFRAME = pandas.read_excel(accounting_data_file, usecols = COMPARISON_COLUMNS)
    except ValueError:
        messagebox.showerror(title = "Oops!", message = "Please check the file used is correct.")
    else:
        messagebox.showinfo(title = "Uploaded!", message = "Accounting file uploaded.")
#--Compare employer submission and transactional recordkeeping data--#
def compare():
    global CONTRACTS_CONTAINER
    comparison_df = EMPLOYER_SUBMISSION_DATA_DATAFRAME.merge(RECORDKEEPING_DATA_DATAFRAME, how = "outer")
    comparison_df = comparison_df.fillna(0)
    comparison_df["Submission vs Recordkeeping"] = comparison_df["Submission Amount"] - comparison_df["Transaction Amount"]
    loan_repayment_df = comparison_df[comparison_df["Contribution Type"] == "Loan Repayment"].merge(ACCOUNTING_DATA_DATAFRAME[ACCOUNTING_DATA_DATAFRAME["Transaction Category"] == "MOF"], how = "outer")
    comparison_df = comparison_df.merge(loan_repayment_df, how = "outer")
    comparison_df = comparison_df.fillna(0)
    try:
        for contract in CONTRACTS_CONTAINER:
            contract_comparison_df = comparison_df[comparison_df["Contract"] == contract]
            contract_submission_df = EMPLOYER_SUBMISSION_DATA_DATAFRAME[EMPLOYER_SUBMISSION_DATA_DATAFRAME["Contract"] == contract]
            contract_recordkeeping_df = RECORDKEEPING_DATA_DATAFRAME[RECORDKEEPING_DATA_DATAFRAME["Contract"] == contract]
            contract_accounting_df = ACCOUNTING_DATA_DATAFRAME[ACCOUNTING_DATA_DATAFRAME["Contract"] == contract]
            date_time = datetime.now().strftime("%m_%d_%y-%I-%M-%S-%p")
            with pandas.ExcelWriter(f"./Output/Contract {contract} Payroll Reconciliation {date_time}.xlsx") as excel_writer:
                contract_comparison_df.to_excel(excel_writer, sheet_name = "Comparison", index = False)
                contract_submission_df.to_excel(excel_writer, sheet_name = "Submission Data", index = False)
                contract_recordkeeping_df.to_excel(excel_writer, sheet_name = "Recordkeeping Data", index = False)
                contract_accounting_df.to_excel(excel_writer, sheet_name = "Accounting Data", index = False)
        messagebox.showinfo(title = "Files Generated", message = "Output files have been generated in the folder: 'Output'")
    except:
        messagebox.showerror(title = "Oops!", message = "Something went wrong.")
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
    CONTRACTS_CONTAINER = []
    for file in FILE_NAME_CONTAINER:
        file.config(text = "")
    messagebox.showinfo(title = "Reset", message = "All files have been cleared from the program.")
#----Application Window Management----#
mainapp = Tk()
mainapp.geometry("600x300")
mainapp.title("Payroll Reconciliation")
mainapp.config(bg = "#000D6B")
employer_submission_label = Label(text = "Employer Submission Spreadsheet: ")
employer_submission_button_border = tkinter.Frame(mainapp, highlightbackground = "#99DDCC", highlightthickness = 2, bd = 0)
employer_submission_button = tkinter.Button(employer_submission_button_border, text = "Upload", command = employer_submission_data_file_upload, bg = "#9C19E0", fg = "#FF5DA2", relief = "flat")
employer_submission_file_name = Label()
FILE_NAME_CONTAINER.append(employer_submission_file_name) 
employer_submission_label.grid(row = 0, column = 0)
employer_submission_button_border.grid(row = 0, column = 1)
employer_submission_button.grid(row = 0, column = 1)
employer_submission_file_name.grid(row = 0, column = 2)
recordkeeping_label = Label(text = "Recordkeeping Data Spreadsheet: ")
recordkeeping_button = Button(text = "Upload", command = recordkeeping_data_file_upload)
recordkeeping_file_name = Label()
FILE_NAME_CONTAINER.append(recordkeeping_file_name) 
recordkeeping_label.grid(row = 1, column = 0)
recordkeeping_button.grid(row = 1, column = 1)
recordkeeping_file_name.grid(row = 1, column = 2)
accounting_label = Label(text = "Contract Accounting Spreadsheet: ")
accounting_button = Button(text = "Upload", command = accounting_data_file_upload)
accounting_file_name = Label()
FILE_NAME_CONTAINER.append(accounting_file_name) 
accounting_label.grid(row = 3, column = 0)
accounting_button.grid(row = 3, column = 1)
accounting_file_name.grid(row = 3, column = 2)
compare_button = Button(text = "Compare Spreadsheets", command = compare)
compare_button.grid(row = 4, column = 0, columnspan = 2)
reset_button = Button(text = "Restart", command = reset)
reset_button.grid(row = 4, column = 2)
output_directory = path.join(CURRENT_DIRECTORY, r"Output")
if not path.exists(output_directory):
    makedirs(output_directory)
mainapp.mainloop()
