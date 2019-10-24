

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


### Delete Function ###
def deleteData():
    while True:
        to_delete = input("Please type the name of the column you wish to delete: ")
        # Checks if input matches data in an existing cell
        if to_delete in user_data:
            user_data.remove(to_delete)
            print("The {} column was removed successfully.".format(to_delete))
            return user_data
        print("A column called \"{}\" could not be found in the data set. Please try again.".format(to_delete))


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

        list_of_listboxes.append(rename_listbox


### Rename Function ###
def renameColumn():
    while True:
        column_name = input("Please type the name of the column you wish to rename: ")
            # Checks if input matches an existing column name
            if column_name in user_data:
                # Ask user for replacement value
                new_column_name = input("Please enter a new name for the {} column: ".format(column_name))
                # Assign the new value to the column's name field
                replaced = [user_data.replace(column_name, new_column_name) for item in user_data]
                print("Success! Column {} has been renamed to {}.".format(column_name, new_column_name))
                return replaced
            # If the input has no match, returns to input request
            print("A column named \"{}\" could not be found. Please try again.".format(column_name))

#%%

        #######################
        #rearrange tab building
        #######################
        # Adds tab 2 of the notebook
        rearrange_tab = ttk.Frame(nb)
        nb.add(rearrange_tab, text='Rearrange')


### Rearrange Function ###
def rearrangeData():
    while True:
        # Asks user to re-order columns into desired arrangement via list indices
        new_order_list = [int(x) for x in input("Data columns are numbered beginning from zero. Thus, five columns would be numbered " +
        "by 0 through 4. Enter your new desired order, separated by spaces (ex: 1 3 0 2 4). Please only enter numbers: ").split()]
        # Checks if all items entered into list are integers
        if all(isinstance(x, int) for x in new_order_list):
            reordered = [reordered[i] for i in new_order_list]
            # Returns user's desired arrangement
            return reordered
        # If they're not all integers, returns to input request
        print("There's an invalid item in your order entry. Please use only integers and try again.")


#%%

        #######################
        #filter tab building
        #######################
        # Adds tab 2 of the notebook
        filter_tab = ttk.Frame(nb)
        nb.add(filter_tab, text='Filter')


### Filter Function ###
def filterData():
    while True:
        filter_key = input("Enter a word, character or number to filter by: ")
        # Check if filter_key is an integer. If so, the try block executes.
        try:
            val = int(filter_key)
            # If value exists in list
            if val in user_data:
                print("Finding all instances of {}.".format(val))
                filtered_output = list(filter(lambda x: x == val, user_data))
                return filtered_output
            else:
                print("Sorry, but {} was not found in the data.".format(val))
                continue
        # If input is not an integer, exception block executes.
        except valueError:
            val = filter_key
            # If value exists in list
            if val in user_data:
                print("Finding all instances of {}.".format(val))
                filtered_output = list(filter(lambda x: x == val, user_data))
                return filtered_output
            else:
                print("Sorry, but {} was not found in the data.".format(val))
                continue

#%%

        #######################
        #sort tab building
        #######################
        # Adds tab 2 of the notebook
        sort_tab = ttk.Frame(nb)
        nb.add(sort_tab, text='Sort')


### Sort Function ###
def sortData():
    while True:
        sort_preference = input("Sort data in Ascending or Descending order? (A/D): ")
        #Ascending Order sort
        if sort_preference == 'A' or sort_preference == 'a':
            user_data.sort()
            return user_data
        #Descending Order sort
        elif sort_preference == 'D' or sort_preference == 'd'
            user_data.sort(reverse=True)
            return user_data
        # If input is invalid
        print("Invalid entry. Please enter \'A\' for Ascending or \'D\' for Descending.")


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
