

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
from collections import OrderedDict

import pickle


#%%

class MyWindow:



    pd.set_option("display.max_columns", 101)

    field_list = []
    frame_list = []
    interior_frame_list = []
    filename = None
    sort_var_list = OrderedDict()
    delete_var_list = OrderedDict()
    loaded_file = False

#%%
    def __init__(self, parent):

        #initialize PMW module for scollable frame widget
        Pmw.initialise(parent)



        self.parent = parent
        self.df = None

##this is causing the set_raddio function to be the same for all frames
#        self.v = StringVar(parent)
#        self.v.set("N") # initialize

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

        button = tk.Button(bottom_frame, text='Export File', command=self.export)
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Create Template', command=self.create_template)
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Load Template', command=self.load_template)
        button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Move field', command=self.rearrange_field)
        self.button.pack(side = tk.LEFT)


##used during testing
#        self.button = tk.Button(bottom_frame, text='Print Frame List', command=self.display_frame_list)
#        self.button.pack(side = tk.LEFT)
##used during testing
#        self.button = tk.Button(bottom_frame, text='Print Frame NAME List', command=self.display_frame_name_list)
#        self.button.pack(side = tk.LEFT)

        #scrollbar
        self.sc = Pmw.ScrolledFrame(self.parent, usehullsize=1, hull_height = 450)
        self.sc.pack(anchor = NW, fill = BOTH)


#        self.df = pd.read_csv(r'C:\Users\jpmul\Desktop\Test file.csv')



#%%

#used during testing
    def display_frame_list(self):
        print(self.frame_list)

    def display_frame_name_list(self):
        print("display_frame_name_list")
        for frame in self.frame_list:
            print(frame.name.get())

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
            self.insert_columns()

                #RENAME
####################################


#need to put in loops to build all these functions into each column's interface
                #filter
                #rearrange
                #groupby
                #pivot


####################################



########
                #need to pu these back into play.  i commented out during testing

#                #create rename box
#                string_var = StringVar()
#                rename_Entry = Entry(left_frame, text='Rename',textvariable=string_var).pack(side = tk.BOTTOM)
#
#         
#


                #create text area for display.  on top of current frame
               



    def insert_columns(self): 
        field_list = list(self.df.columns)

            #create a new frame with each field
        for field in field_list:
            #create new frame instance, pass field name as frame name
            #duplicate field names is going to cause issues
            my_frame = MyFrame()
            my_frame._init_(field)

            #add to list of frames so you can later iterate
            self.frame_list.append(my_frame)

            #master=self.parent is causing it to be in botton of frame
            left_frame = tk.LabelFrame(self.sc.interior(),text=field)
            left_frame.pack(side=tk.LEFT)
            self.interior_frame_list.append(left_frame)


            #SORT FUNCTION
            #sort modes for radio button widget
            modes = [('Sort Ascending','A'),('Sort Descending','D'),('Do Not Sort','N')]
            for text, mode in modes:
                b = Radiobutton(left_frame, text=text, variable=my_frame.sort_var, value=mode, indicatoron =0)
                b.pack(side=tk.BOTTOM,anchor=W)


            #FILTER FUNCTION

            #REARRANGE

            #DELETE
            b = Checkbutton(left_frame, text='Delete', variable = my_frame.delete_var, onvalue = 'D', offvalue = 'N' )
            b.pack(side=BOTTOM, anchor = W)

            #RENAME


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



#%%
    def create_var_lists(self):

        #loop through frames to create variable list
        for frame in self.frame_list:

            #sort function
            frame_name = frame.name.get()
            sort_var = frame.sort_var.get()
            self.sort_var_list.update({frame_name:sort_var})

            #delete
            delete_var = frame.delete_var.get()
            self.delete_var_list.update({frame_name:delete_var})

            #rename

            #filter



#        print(self.sort_var_list)

#%%
    def preview(self):
        if self.df is not None:
            #first, create all the variable lists
            if self.loaded_file == False:
                self.create_var_lists()
            else:
                #reset loaded file to false so you can make edits and still preview
                self.loaded_file = False

            #go through each function
            self.sort_field()
            self.delete_field()

            #print out during testing
            print(self.df)
            self.update_window()
        else:
            messagebox.showinfo("Error", "Please load data to preview.")

    #Update the scrolled frame holding the columns
    def update_window(self): 
        for frame in self.interior_frame_list:
            frame.pack_forget()
        self.insert_columns()



#%%
    def sort_field(self):
        #loop through the sort list
        for key in self.sort_var_list:
            sort_order = self.sort_var_list.get(key)
            if sort_order == "A":
                self.df.sort_values(by=key, ascending=True,inplace=True, kind='mergesort')
            elif sort_order == "D":
                self.df.sort_values(by=key, ascending=False,inplace=True, kind='mergesort')



#%%
    def create_template(self):
        #create variable lists from current settings
        self.create_var_lists()

        #dump file
        #need to write in save file dialogue after testing
        #we need to dump every single variable list
            #do we just make a list of lists?
            #and then peel it apart afteward/on loading
        pickle.dump(self.sort_var_list, open( "save_template.p", "wb" ) )





#%%
    def load_template(self):

        #need to put in open dialogue prompt after testing
        #and we'll need to loop through all variable lists
        self.loaded_file = True
        self.sort_var_list = pickle.load(open( "save_template.p", "rb" ) )
        self.preview()


#%%
    def group_by(self):

        #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            group_field = simpledialog.askstring("Group By", "Which field to group by?",
                                parent=self.parent)
            self.df = self.df.groupby(group_field).count()



#%%
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




#%%
    def delete_field(self):
        for item in self.delete_var_list:
            delete = self.delete_var_list.get(item)
            if(item in self.df.columns):
                if(delete == 'D'):
                    self.df = self.df.drop(columns = item)



    
#%%
    def filter_field(self):
            #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Filter Field", "Field to filter?",
                                                parent=self.parent)
            filter_value = simpledialog.askstring("Filter Field", "Filter for what?",
                                                  parent=self.parent)
            self.df = self.df[self.df[field_name] == filter_value]

#%%
    def rename_field(self):
            #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Rename Field", "Field to rename?",
                                                parent=self.parent)
            rename_value = simpledialog.askstring("Rename Field", "Enter new name",
                                                  parent=self.parent)
            self.df.rename(columns={field_name:rename_value}, inplace=True)




#%%


    def rearrange_field(self):
        columns = self.swap_fields()
        self.df.columns = columns
        self.update_window()


#Function swap_fields
#Prompts user to swap two columns
#Returns a list with new column orders
    def swap_fields(self):
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
    def export(self):
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
                # If input file extension does not match
                messagebox.showerror("Error", "Invalid filetype. Please try again.", parent=self.parent)
        # If no dataframe has been created yet
        messagebox.showerror("Error", "No data has been loaded yet!", parent=self.parent)

#%%
            #have to make an object for each frame

class MyFrame:



    def _init_(self,field):
#        super()._init_(parent)
#        self.parent = parent
        self.name = StringVar()
        self.name.set(field)
#        print("this is from the frame _init_ function")
#        print(self.name.get())

        self.sort_var = StringVar()
        self.sort_var.set("N")

        #do all the same as above for each function's variable need

        #DELETE FUNCTION
        self.delete_var = StringVar()
        self.delete_var.set('N')

        #FILTER FUNCTION

        #RENAME FUNCTION



#%%

#    def sort_order(self):
#        print(self.name + '_')
#        print(self.sort_var.get())



#%%
# --- main ---

if __name__ == '__main__':



    #create root window
    root = tk.Tk()
    root.title('Spreadhsheet Miracle Machine Demo')
    root.geometry('1000x500')

    top = MyWindow(root)


    root.mainloop()
