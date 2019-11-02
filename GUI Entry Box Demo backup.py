

#%%
import pandas as pd

from pandas.api.types import CategoricalDtype
import xlsxwriter
from tkinter import *
pd.get_option('display.max_columns')
pd.set_option('display.max_columns',None)
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import scrolledtext
import matplotlib.pyplot as plot


#%%

class MyWindow:

#    pd.set_option(display.max_columns = 20)
#    pd.display.options.max_columns = 20
#    pd.set_option("display.max_columns", 101)
    pd.get_option('display.max_columns')
    pd.set_option('display.max_columns',None)


    def __init__(self, parent):

        self.parent = parent

        self.filename = None
        self.df = None
#        self.set_option('display.max_colwidth', 0)


        top_frame = tk.Frame(self.parent)
        top_frame.pack(side=tk.TOP)

#        self.text = scrolledtext.ScrolledText(top_frame,width=1000,wrap="none")
        self.text = scrolledtext.ScrolledText(top_frame,width=1000,wrap="none")

        self.text.pack(side=tk.TOP)

        bottom_frame = tk.Frame(self.parent)
        bottom_frame.pack(side = tk.BOTTOM)

        self.button = tk.Button(bottom_frame, text='Load File', command=self.load)
        self.button.pack(side = tk.LEFT)

#        self.button = tk.Button(bottom_frame, text='Display Data', command=self.display)
#        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Group By', command=self.group_by)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Pivot', command=self.pivot)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Delete Field', command=self.delete_field)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Filter field', command=self.filter_field)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Rename field', command=self.rename_field)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Sort field', command=self.sort_field)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Export Data', command=self.export_data)
        self.button.pack(side = tk.LEFT)

    def create_field_list(self):
        if self.df is not None:
            field_list = []
            for col in self.df.columns:
                field_list.append(col)
            return field_list

    def make_columns(self):
        if self.df is not None:
            field_list = self.create_field_list
            i = 0
            while i < len(field_list):
                radio1 = tk.Radiobutton(self.parent, text = "Delete")
                radio1.grid(row=0,column=i)
                radio2 = tk.Radiobutton(self.parent, text = "ReName")
                radio2.grid(row=1,column=i)


    def load(self):
        #get filename for opening
        name = fd.askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])

        #make sure name is populated
        if name:
            #if csv, use read_csv to create the self.dataframe
            if name.endswith('.csv'):
                self.df = pd.read_csv(name)
            #otherwise, it must be an excel file
            else:
                self.df = pd.read_excel(name)
            #save the filename for reference
            self.filename = name
            self.display()


    def display(self):
        #clear field first
        self.text.delete(1.0,END)
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            self.text.insert('end', str(self.df) + '\n')


    def group_by(self):

        #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            group_field = simpledialog.askstring("Group By", "Which field to group by?",
                                parent=self.parent)
            self.df = self.df.groupby(group_field).count()
        self.display()

    def pivot(self):

        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            index_field = simpledialog.askstring("Pivot", "Rows?",
                                                 parent=self.parent)
            column_field = simpledialog.askstring("Pivot", "Columns?",
                                                 parent=self.parent)
            pivot_values = simpledialog.askstring("Pivot", "Values?",
                                parent=self.parent)
            #agg_func isn't working when passed into the pivot function - don't know how this can be done
#            agg_func = simpledialog.askstring("Pivot", "What aggregation? Count, Sum, Max, Min, etc",
#                                              parent=self.parent)

            self.df = pd.pivot_table(self.df, index=index_field, columns=column_field, values = pivot_values,
                                     dropna=False,aggfunc='count')

        self.display()


    def delete_field(self):
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Delete Field", "Field to delete?",
                                parent=self.parent)
            self.df = self.df.drop(columns = field_name)
        self.display()

    def filter_field(self):
            #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Filter Field", "Field to filter?",
                                                parent=self.parent)
            filter_value = simpledialog.askstring("Filter Field", "Filter value:",
                                                  parent=self.parent)
            self.df = self.df[self.df[field_name] == filter_value]
        self.display()


    def rename_field(self):
            #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Rename Field", "Field to rename?",
                                                parent=self.parent)
            rename_value = simpledialog.askstring("Rename Field", "Enter new name",
                                                  parent=self.parent)
            self.df.rename(columns={field_name:rename_value}, inplace=True)
        self.display()

    def sort_field(self):
            #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Sort Field", "Field to sort?",
                            parent=self.parent)
            sort_preference = simpledialog.askstring("Sort Field",
                                                     "Sort data in Ascending or Descending order? (A/D): ",
                                                     parent=self.parent)
            #Ascending Order sort
            if sort_preference == 'A' or sort_preference == 'a':
                self.df.sort_values(by=field_name, ascending=True, inplace=True, kind='mergesort')
            #Descending Order sort
            elif sort_preference == 'D' or sort_preference == 'd':
                self.df.sort_values(by=field_name, ascending=False,inplace=True, kind='mergesort')
        self.display()


    def export_data(self):
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            while True:
                filetype_choice = simpledialog.askstring("Desired format", "Save as CSV, XLSX, or PDF?",
                    parent=self.parent)
                if filetype_choice == 'CSV' or filetype_choice == 'csv':
                    #open sys file dialog to save
                    export_name = fd.asksaveasfilename(filetypes = [('CSV', '*.csv',)])
                    self.df.to_csv(export_name + '.csv', index=None, header=True)

                    return
                elif filetype_choice == 'XLSX' or filetype_choice == 'xlsx':
                    #open sys file dialog to save
                    export_name = fd.asksaveasfilename(filetypes = [('Excel', ('*.xls', '*.xlsx'))])
                    self.df.to_excel(export_name + '.xlsx', index=False)

                    return
                elif filetype_choice == 'PDF' or filetype_choice == 'pdf':
                    # self.df.to_html('out.html')
                    export_name = simpledialog.askstring("Input", "File name: ",
                    parent=self.parent)
                    pdf_name = export_name + '.pdf'
                    plotted = self.df.plot()
                    plotted.get_figure().savefig(pdf_name)
                    return
                # If input file extension does not match
                messagebox.showerror("Error", "Invalid filetype. Please try again.", parent=self.parent)
        # If no dataframe has been created yet
        messagebox.showerror("Error", "No data has been loaded yet!", parent=self.parent)



#%%
# --- main ---

if __name__ == '__main__':
    pd.get_option('display.max_columns')
    pd.set_option('display.max_columns',None)
    root = tk.Tk()
    root.title('Notebook Demo')
    root.geometry('650x500')

    top = MyWindow(root)



    root.mainloop()



