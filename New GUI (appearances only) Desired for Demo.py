

#%%
import pandas as pd
from pandas.api.types import CategoricalDtype
import xlsxwriter
from tkinter import *
import Pmw

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import simpledialog
from tkinter import messagebox

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
        
        #initialize PMW module for scollable frame widget
        Pmw.initialise(parent)

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

        self.parent = parent
        self.df = None
#        self.filename = filename
#        self.original_df = df
#        self.df = df

#    def set_filename(filename):
#        self.filename = filename
#    def get_filename():
#        return self.filename

        #create bottom frame
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(side = tk.BOTTOM)

        #add buttons
        button = tk.Button(bottom_frame, text='Load New File', command= lambda: load(self))
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Revert to Original', command=load)
        button.pack(side = tk.LEFT)

        #SHOULD WE MAKE ALL OF THE BELOW TABS??
            #then, when we execute something, they can pull the variables from the main tab?

        #display the dataframe with changes as they sit in the window
        #do we want to show in a new window?
        button = tk.Button(bottom_frame, text='Preview Changes', command=load)
        button.pack(side = tk.LEFT)

        #prompt to save/export to PDF, etc
        button = tk.Button(bottom_frame, text='Export File', command=load)
        button.pack(side = tk.LEFT)

        #this will want to pop open another window
        button = tk.Button(bottom_frame, text='Create Template', command=load)
        button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Move field', command=self.rearrange_field)
        self.button.pack(side = tk.LEFT)


#        field_list = self.create_field_list


        self.sc = Pmw.ScrolledFrame(self.parent, usehullsize=1, hull_height = 450)
        self.sc.pack(anchor = NW, fill = BOTH)

#        field_list = ['ColumnA','ColumnB','ColumnC']
        self.df = pd.read_csv(r'C:\Users\Jeremy\Desktop\A working file\Test file.csv')
        if self.df is not None:
            field_list = list(self.df.columns)


        #make buttons/boxes for every column, and display some records
            for field in field_list:
    #            left_frame = tk.Frame(self.parent,width=2,relief=tk.SUNKEN,highlightcolor='black')
                left_frame = tk.LabelFrame(self.sc.interior(),text=field)
                left_frame.pack(side=tk.LEFT)



    #           #sort radio buttons
                modes = [('Sort Ascending','A'),('Sort Descending','D'),('Do Not Sort','N')]
                v = StringVar()
                v.set("N") # initialize

                for text, mode in modes:
                    b = Radiobutton(left_frame, text=text,
                            variable=v, value=mode)
                    b.pack(side=tk.BOTTOM,anchor=W)


                #filter
                #rearrange
                #groupby
                #pivot

                #create rename box
                string_var = StringVar()
                rename_Entry = Entry(left_frame, text='Rename',textvariable=string_var).pack(side = tk.BOTTOM)

                #create delete box
                int_var = IntVar()
                delete_checkbutton = Checkbutton(left_frame, text='Delete', variable=int_var).pack(side = tk.BOTTOM)



                #create text area for display.  on top of current frame
                self.text = tk.Text(left_frame,width=20, height = 17)
                self.text.pack(side=tk.BOTTOM)
                #for the current field, get the contents in a df
                col_df = self.df[field]

                self.text.insert('end', str(col_df) + '\n')






#        for field in field_list:
#            int_var = IntVar()
#            check_button = Checkbutton(parent, text=field, variable=int_var).pack(side = tk.LEFT)

#        top_frame = tk.Frame(self.parent)
#        top_frame.pack(side=tk.TOP)
#
#        self.text = tk.Text(top_frame)
#        self.text.pack(side=tk.TOP)
#
#        bottom_frame = tk.Frame(self.parent)
#        bottom_frame.pack(side = tk.BOTTOM)
##
#        self.button = tk.Button(bottom_frame, text='Load File', command=self.load)
#        self.button.pack(side = tk.LEFT)

#        self.button = tk.Button(bottom_frame, text='Display Data', command=self.display)
#        self.button.pack(side = tk.LEFT)

#        self.button = tk.Button(bottom_frame, text='Group By', command=self.group_by)
#        self.button.pack(side = tk.LEFT)
#
#        self.button = tk.Button(bottom_frame, text='Pivot', command=self.pivot)
#        self.button.pack(side = tk.LEFT)
#
#        self.button = tk.Button(bottom_frame, text='Delete Field', command=self.delete_field)
#        self.button.pack(side = tk.LEFT)
#
#        self.button = tk.Button(bottom_frame, text='Filter field', command=self.filter_field)
#        self.button.pack(side = tk.LEFT)
#
#        self.button = tk.Button(bottom_frame, text='Rename field', command=self.rename_field)
#        self.button.pack(side = tk.LEFT)
#
#        self.button = tk.Button(bottom_frame, text='Sort field', command=self.sort_field)
#        self.button.pack(side = tk.LEFT)
#
#        self.button = tk.Button(bottom_frame, text='Move field', command=self.rearrange_field)
#        self.button.pack(side = tk.LEFT)


    def create_field_list(self):
        #i think you can just use df.columns.tolist here, so no looping
        # or this -> cols = list(df.columns.values)
        # or this -> list(df.columns)
        if self.df is not None:
            field_list = list(self.df.columns)
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





    def display(self):
        #clear field first
        self.text.delete(1.0,END)
        #make sure there's a daaframe loaded, otherwise, do nothing
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

        #make sure there's a daaframe loaded, otherwise, do nothing
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
        #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Delete Field", "Field to delete?",
                                parent=self.parent)
            self.df = self.df.drop(columns = field_name)
        self.display()

    def filter_field(self):
            #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Filter Field", "Field to filter?",
                                                parent=self.parent)
            filter_value = simpledialog.askstring("Filter Field", "Filter for what?",
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




#Function Rearrange_field
#Prompts user to swap two columns
#Returns a list with new column orders
    def rearrange_field(self):
        #make sure there's a daaframe loaded; otherwise, do nothing
        if self.df is not None:
            #Create list of current column orders
            field_list = self.create_field_list()
            
            #Prompt user for the Name of the Column to move, this will continue until the user cancels or inputs a correct CASE SENSITIVE field name
            #Cancel will return the current field name list
            field_name = simpledialog.askstring("Rearrange Fields", "Field to move?",
                            parent=self.parent)
           
            while field_name not in field_list and field_name != None:
                field_name = simpledialog.askstring("Rearrange Fields", "Field does not exist. Try again", parent=self.parent)
                if field_name == None:
                    break
           
            if(field_name == None):
                    return field_list

            #Prompt user for the Name of the Column to we wish to move the selected column behind, this will continue until the user cancels or inputs a correct CASE SENSITIVE field name
            #Cancel will return the current field name list
            before_field = simpledialog.askstring("Rearrange Fields", "Put before this field (enter field name)", parent=self.parent)
           
            while before_field not in field_list and before_field != None:
               before_field = simpledialog.askstring("Rearrange Fields", "Field does not exist. Try again", parent=self.parent)
               if before_field == None:
                    break
            
            if(before_field == None):
                return field_list
            
            #Handles moving the column behind the second column and returns a new list of columns
            if messagebox.askokcancel("Confirm","Move " + field_name + " behind " + before_field):
                new_list = field_list.copy()
                new_list.remove(field_name)
                new_list.insert(new_list.index(before_field) + 1, field_name)
                return new_list






#%%
# --- main ---

if __name__ == '__main__':



    #create root window
    root = tk.Tk()
    root.title('Spreadhsheet Miracle Machine Demo')
    root.geometry('1000x500')

    top = MyWindow(root)







#    scrollbar = Scrollbar(root)
#    scrollbar.pack(side=RIGHT, fill=Y)
#    listbox = Listbox(master, yscrollcommand=scrollbar.set)
#    for i in range(1000):
#        listbox.insert(END, str(i))
#    listbox.pack(side=LEFT, fill=BOTH)
#
#    scrollbar.config(command=listbox.yview)
#
#
#
#
#    scrollbar = Scrollbar(root)
#    scrollbar.pack(side=RIGHT, fill=Y)
#    scrollbar = Scrollbar(root)
#    scrollbar.pack(side=BOTTOM, fill=Y)





    root.mainloop()



