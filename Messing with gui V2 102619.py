

#%%
import pandas as pd
from pandas.api.types import CategoricalDtype
import xlsxwriter
from tkinter import *

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import simpledialog

#%%

def get_file_extension(filename):
    #gives the file extension, without the period
    file_extension = os.path.splitext(filename)[1][1:]
    print(filename)
    print(file_extension)
    return file_extension


#%%
def create_original_df(filename):
    #will need to determine filetype
    file_extension = get_file_extension(filename)

    if (file_extension == 'csv'):
        original_df = pd.read_csv(filename)
    elif (file_extension == 'xlsx'):
        original_df = pd.read_excel
    else:
        #have to figure out what to return here, or do we somehow send back to file dialog?
        return('Bad File Extension, please reselect file')

    #we want to

    #we want to return the original dataframe
    return original_df


#%%
def get_filename():
    #ideally, you would point this to the central repository
        #right now it just opens in C:/
#    fd.askopenfilename()

    filename = fd.askopenfilename(filetypes = (("Excel files","*.xlsx"),(".csv files","*.csv")))
#    print(filename)
    #double check the file extension
    file_extension = get_file_extension(filename)
#    print(file_extension)

    #loop until they pick a file or hit cancel
        #i don't have the cancel part working, so it just keeps looping until they
        #pick a good file
    while file_extension not in ['csv','xlsx']:
        #message box to return error or try again
        filename = fd.askopenfilename()
#        print(file_extension)
        file_extension = get_file_extension(filename)
#        print(filename)

    #send filename to have the original file read into a df
    create_original_df(filename)

    #load into main view

#create main window object
    #i don't know what the screenName does

#%%




#main = Tk()
#main.title('Notebook Demo')
#main.geometry('750x750')
#
#
## gives weight to the cells in the grid
#rows = 0
#while rows < 50:
#    main.rowconfigure(rows, weight=1)
#    main.columnconfigure(rows, weight=1)
#    rows += 1
#
## Defines and places the notebook widget
#nb = ttk.Notebook(main)
#nb.pack()
##nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')
#
## Adds tab 1 of the notebook
#page1 = ttk.Frame(nb)
#nb.add(page1, text='Tab1')
#
## Adds tab 2 of the notebook
#page2 = ttk.Frame(nb)
#nb.add(page2, text='Tab2')
#
#
#
#main.mainloop()
#%%

class MyWindow:

#    pd.set_option(display.max_columns = 20)
#    pd.display.options.max_columns = 20
    pd.set_option("display.max_columns", 101)
    def __init__(self, parent):

        self.parent = parent

        self.filename = None
        self.df = None

#        scroll = Scrollbar(root)
#        scroll.grid(column = 50)

#        tree = ttk.Treeview(self.parent)


        top_frame = tk.Frame(self.parent)
        top_frame.pack(side=tk.TOP)

        self.text = tk.Text(top_frame)
        self.text.pack(side=tk.TOP)
#
#        self.text = tk.Text(self.parent)
#        self.text.pack(side=tk.TOP)


        bottom_frame = tk.Frame(self.parent)
        bottom_frame.pack(side = tk.BOTTOM)


#        radio1 = tk.Radiobutton(self.parent, text = "Delete")
#        radio1.grid(row=0,column=0)

        self.button = tk.Button(bottom_frame, text='Load File', command=self.load)
        self.button.pack(side = tk.LEFT)


        self.button = tk.Button(bottom_frame, text='Display Data', command=self.display)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Group By', command=self.group_by)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Pivot', command=self.pivot)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Delete Field', command=self.delete_field)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Filter a field', command=self.filter_field)
        self.button.pack(side = tk.LEFT)

#        preview_file =
#        self.button = tk.Button(self.parent, text='Preview', command=self.Preview)
#        self.button.grid()


#    def preview(self):
#        if self.df is not None:

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
#            self.display()
#            self.make_columns

    def display(self):
        #clear field first
        self.text.delete(1.0,END)
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            #this just keeps displaying a new head below the last
            #we want to remove the existing and then display
            #leave it for testing though, you can see the changes this way
#            self.text.insert('end', self.filename + '\n')
#            self.text.insert('end', str(self.df.head(20)) + '\n')
            self.text.insert('end', str(self.df) + '\n')


    def group_by(self):

        #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            group_field = simpledialog.askstring("Input", "Which field to group by?",
                                parent=self.parent)
            self.df = self.df.groupby(group_field).count()
        self.display()

    def pivot(self):

        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            listbox = tk.Listbox(self.parent,selectmode='extended')
            listbox.grid(row=0,column=0)
            field_list = self.create_field_list

            for item in [field_list]:
                listbox.insert(END, item)




#            index = simpledialog.askstring("Input", "Rows?",
#                                parent=self.parent)
#            values = simpledialog.askstring("Input", "Values?",
#                                parent=self.parent)

            #need to figure out a way to ask what type of aggregation function

            #create pivot
#            self.df = pd.pivot_table(self.df, index=index, values = values, aggfunc='count', dropna=False)
#        self.display()



    def delete_field(self):
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
#            listbox = Listbox(self,self.parent,selectmode='extended')
#            field_list = self.create_field_list
#            for item in [field_list]:
#                listbox.insert(END, item)
            field_name = simpledialog.askstring("Input", "Field to delete?",
                                parent=self.parent)
            self.df = self.df.drop(columns = field_name)
        self.display()

    def filter_field(self):
            #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Input", "Field to filter?",
                            parent=self.parent)
            filter_value = simpledialog.askstring("Input", "Filter for what?",
                            parent=self.parent)
            self.df = self.df[self.df[field_name] == filter_value]
#                self.df = self.df.filter(like=filter_value, axis = 0)
        self.display()

#%%

##%%
#def load():
#
#    name = fd.askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])
#
#    if name:
#        if name.endswith('.csv'):
#            df = pd.read_csv(name)
#        else:
#            df = pd.read_excel(name)
#
##            df.filename = name
#
##%%
#def display():
#    # ask for file if not loaded yet
#    if df is None:
#        load()
#
#    # display if loaded
#    if df is not None:
#        #this just keeps displaying a new head below the last
#        #we want to remove the existing and then display
#        df.text.insert('end', df.filename + '\n')
#        df.text.insert('end', str(df.head()) + '\n')


#%%
# --- main ---

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Notebook Demo')
    root.geometry('500x500')

    top = MyWindow(root)

    root.mainloop()



