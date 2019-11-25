

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

class MyWindow:



    pd.set_option("display.max_columns", 101)

    field_list = []
    frame_list = []
    v = None
#%%
    def __init__(self, parent):

        #initialize PMW module for scollable frame widget
        Pmw.initialise(parent)



        self.parent = parent
        self.df = None


        #create bottom frame
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(side = tk.BOTTOM)

        #add buttons
        button = tk.Button(bottom_frame, text='Load New File', command=self.load)
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Revert to Original', command=self.load)
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Preview Changes', command=self.preview)
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Export File', command=self.load)
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Create Template', command=self.load)
        button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Move field', command=self.rearrange_field)
        self.button.pack(side = tk.LEFT)


        #scrollbar
        self.sc = Pmw.ScrolledFrame(self.parent, usehullsize=1, hull_height = 450)
        self.sc.pack(anchor = NW, fill = BOTH)


#        self.df = pd.read_csv(r'C:\Users\jpmul\Desktop\Test file.csv')


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

        if self.df is not None:
            field_list = list(self.df.columns)


        #make buttons/boxes for every column, and display some records
            for field in field_list:
    #            left_frame = tk.Frame(self.parent,width=2,relief=tk.SUNKEN,highlightcolor='black')
                left_frame = tk.LabelFrame(self.sc.interior(),text=field)
                left_frame.pack(side=tk.LEFT)

                #add to list of frames so you can later iterate
                self.frame_list.append(left_frame)


    #           #sort radio buttons
                modes = [('Sort Ascending','A'),('Sort Descending','D'),('Do Not Sort','N')]
                v = StringVar()
                v.set("N") # initialize

                for text, mode in modes:
                    b = Radiobutton(left_frame, text=text,
                            variable=v, value=mode, indicatoron =0)
                    b.pack(side=tk.BOTTOM,anchor=W)


                #filter radio button
                



####################################

#create filter box
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            filter_field = StringVar()
            filter_Entry = Entry(left_frame, text='Field to Filter',textvariable=filter_field).pack(side = tk.BOTTOM)
            filter_val = StringVar()
            filter_Entry = Entry(left_frame, text='Filter by what?',textvariable=filter_val).pack(side = tk.BOTTOM)

         #create text area for display, on top of current frame
         self.text = tk.Text(left_frame,width=20, height = 17)
         self.text.pack(side=tk.BOTTOM)

         #for the current field, get the contents in a df
         self.df = self.df[self.df[filter_field] == filter_val]


#create rearrange box
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            #Create list of current column orders
            field_order = self.create_field_list()

            first_field = StringVar()
            first_Entry = Entry(left_frame, text='Field to Move',textvariable=first_field).pack(side = tk.BOTTOM)

            second_field = StringVar()
            second_Entry = Entry(left_frame, text='Field to place it before?',textvariable=second_field).pack(side = tk.BOTTOM)

         #create text area for display, on top of current frame
         self.text = tk.Text(left_frame,width=20, height = 17)
         self.text.pack(side=tk.BOTTOM)

         #for the current field, get the contents in a df
         new_order = field_order.copy()
         new_order.remove(field_name)
         new_order.insert(new_order.index(second_field) + 1, first_field)
         self.df = self.df.replace(new_order)


#create groupby box
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            group_val = StringVar()
            filter_Entry = Entry(left_frame, text='Field to Group by',textvariable=group_val).pack(side = tk.BOTTOM)

         #create text area for display, on top of current frame
         self.text = tk.Text(left_frame,width=20, height = 17)
         self.text.pack(side=tk.BOTTOM)

         #for the current field, get the contents in a df
         self.df = self.df.groupby(group_val).count()


#create pivot box
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            index_chosen = StringVar()
            index_Entry = Entry(left_frame, text='Rows to Pivot',textvariable=index_chosen).pack(side = tk.BOTTOM)
            column_chosen = StringVar()
            column_Entry = Entry(left_frame, text='Columns to Pivot',textvariable=column_chosen).pack(side = tk.BOTTOM)
            pivot_val = StringVar()
            pivot_Entry = Entry(left_frame, text='Pivot by what values?',textvariable=pivot_val).pack(side = tk.BOTTOM)

         #create text area for display, on top of current frame
         self.text = tk.Text(left_frame,width=20, height = 17)
         self.text.pack(side=tk.BOTTOM)

         #for the current field, get the contents in a df
         self.df = pd.pivot_table(self.df, index=index_chosen, columns=column_chosen, values = pivot_val,
                                     dropna=False,aggfunc='count')


####################################





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



#%%
    def create_field_list(self):
        if self.df is not None:
            field_list = list(self.df.columns)
            return field_list

##%%
#    def make_columns(self):
#        if self.df is not None:
#            field_list = self.create_field_list
#            i = 0
#            while i < len(field_list):
#                radio1 = tk.Radiobutton(self.parent, text = "Delete")
#                radio1.grid(row=0,column=i)
#                radio2 = tk.Radiobutton(self.parent, text = "ReName")
#                radio2.grid(row=1,column=i)


#%%
#    def preview(self):
#        for frame in self.frame_list:
#            for child in frame.children.values():
#                print(self.v.get())

#%%
    def preview(self):
        for frame in self.frame_list:
            for child in frame.pack_slaves():
                print(child["variable"])


#%%
#    def preview(self):
#        for frame in self.frame_list:
#            for radio_button in filter(lambda w:isinstance(w,RadioButton), frame.children.itervalues()):
#                print("okay")


#%%
    def group_by(self):

        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            group_field = simpledialog.askstring("Group By", "Which field to group by?",
                                parent=self.parent)
            self.df = self.df.groupby(group_field).count()



#%%
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




#%%
    def delete_field(self):
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Delete Field", "Field to delete?",
                                parent=self.parent)
            self.df = self.df.drop(columns = field_name)

#%%
    def filter_field(self):
            #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Filter Field", "Field to filter?",
                                                parent=self.parent)
            filter_value = simpledialog.askstring("Filter Field", "Filter for what?",
                                                  parent=self.parent)
            self.df = self.df[self.df[field_name] == filter_value]

#%%
    def rename_field(self):
            #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Rename Field", "Field to rename?",
                                                parent=self.parent)
            rename_value = simpledialog.askstring("Rename Field", "Enter new name",
                                                  parent=self.parent)
            self.df.rename(columns={field_name:rename_value}, inplace=True)

#%%
    def sort_field(self):
            #make sure there's a dataframe loaded, otherwise, do nothing
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



#%%

#Function Rearrange_field
#Prompts user to swap two columns
#Returns a list with new column orders
    def rearrange_field(self):
        #make sure there's a dataframe loaded; otherwise, do nothing
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


    root.mainloop()
