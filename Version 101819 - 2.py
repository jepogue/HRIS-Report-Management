

#%%
import pandas as pd
from pandas.api.types import CategoricalDtype
import xlsxwriter
from tkinter import *
from tkinter import ttk
import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import simpledialog



#%%

class MyWindow:




    #%%

#########################
        #functions
############################

    #to get a list of the headers, as we need to display them in dropdowns, etc
    def create_field_list(self):
        if self.df is not None:
            field_list = []
            for col in self.df.columns:
                field_list.append(col)
            return field_list


#%%

    def update_listboxes(self):


        if self.df is not None:
            field_list = self.create_field_list
            for item in field_list:
                listbox.insert(tk.END, "Choice " + item)

#%%

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


#%%

    def display(self):
        #clear field first
        self.text.delete(1.0,tk.END)
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            #don't know how to show all columns, we will need this in our "preview"
            self.text.insert('end', str(self.df.head(50)) + '\n')
#            self.text.insert('end', str(self.df) + '\n')
            update_listboxes(self, list_of_listboxes)

#%%
    def pivot(self):

        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            listbox = tk.Listbox(self.parent,selectmode='extended')
            listbox.grid(row=0,column=0)
            field_list = self.create_field_list

            for item in [field_list]:
                listbox.insert(tk.END, item)



#%%

    pd.set_option("display.max_columns", 101)
    def __init__(self, parent):


        #set parent
        self.parent = parent


        self.filename = None
        self.df = None

        list_of_listboxes = []


        # Defines and places the notebook widget
        nb = ttk.Notebook(root)
        nb.pack(side=tk.TOP)




#%%
        #######################
        #display tab building
        #######################
        # Adds tab 1 of the notebook
        display_tab = ttk.Frame(nb)
        nb.add(display_tab, text='Load/Display')

        #create bottom frame on display tab
        bottom_frame = tk.Frame(display_tab)
        bottom_frame.pack(side = tk.BOTTOM)

        #put buttons on display tab
        self.button = tk.Button(bottom_frame, text='Load File', command=self.load)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text = 'Finalize',command = None)
        self.button.pack(side=tk.RIGHT)

        self.button = tk.Button(bottom_frame, text='Refresh', command=self.display)
        self.button.pack(side = tk.RIGHT)



        #creates a place to populate text in order to display file
        #i don't know how to display the whole file yet - headers get shortened
        self.text = tk.Text(display_tab)
        self.text.pack(side=tk.TOP)


#%%

        #######################
        #deletes tab building
        #######################
        # Adds tab 2 of the notebook
        delete_tab = ttk.Frame(nb)
        nb.add(delete_tab, text='Delete')

        delete_listbox = tk.Listbox(delete_tab, height=4,selectmode = 'extended')
        delete_listbox.pack()
        delete_listbox.insert(tk.END, "PLACEHOLDER ")

        field_list = ['field1','field2','field3','field4''field5','field6','field7']
        for item in field_list:
            delete_listbox.insert(tk.END, item)

        list_of_listboxes.append(delete_listbox)


#%%

        #######################
        #rename tab building
        #######################
        # Adds tab 2 of the notebook
        rename_tab = ttk.Frame(nb)
        nb.add(rename_tab, text='Rename')

        rename_listbox = tk.Listbox(rename_tab, height=4,selectmode = 'extended')
        rename_listbox.pack()
        field_list = ['field1','field2','field3','field4''field5','field6','field7']
        for item in field_list:
            rename_listbox.insert(tk.END, item)

        list_of_listboxes.append(rename_listbox)

#%%

        #######################
        #rearrange tab building
        #######################
        # Adds tab 2 of the notebook
        rearrange_tab = ttk.Frame(nb)
        nb.add(rearrange_tab, text='Rearrange')

#%%

        #######################
        #filter tab building
        #######################
        # Adds tab 2 of the notebook
        filter_tab = ttk.Frame(nb)
        nb.add(filter_tab, text='Filter')


#%%

        #######################
        #sort tab building
        #######################
        # Adds tab 2 of the notebook
        sort_tab = ttk.Frame(nb)
        nb.add(sort_tab, text='Sort')





#%%
# --- main ---

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Spreadsheet Miracle Machine')
    root.geometry('500x500')
        # gives weight to the cells in the grid
    rows = 0
    while rows < 50:
        root.rowconfigure(rows, weight=1)
        root.columnconfigure(rows, weight=1)
        rows += 1


    top = MyWindow(root)

    root.mainloop()

