




#JPM updated 11/29/19
#added pivot function widgets and functinoality
#added another dataframe variable called "df_preview", so that we can preserve the original df
    #this must be referenced in all of the functions to be applied, as well as to export





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
import glob
import pickle


#%%

class MyWindow:



    pd.set_option("display.max_columns", 101)

    #create a dictionary to house all variables and their names
        #we'll need this when pickling/unpickling for template
    variable_list = {}

    field_list = []

    #this is for the "MyFrame" objects
    frame_list = []
    #this is for the actual frames
    widget_frame_list = []

    filename = None

    #contains sort function's variable list
    sort_var_list = OrderedDict()
    variable_list.update({'sort_var_list':sort_var_list})

    #contains the pivot functions lists
        #columns
    pivot_col_var_list = []
    #add to dictionary of variables and their names
    variable_list.update({'pivot_col_var_list':pivot_col_var_list})
        #rows
    pivot_row_var_list = []
    #add to dictionary of variables and their names
    variable_list.update({'pivot_row_var_list':pivot_row_var_list})
        #values
    pivot_value_var_list = []
    #add to dictionary of variables and their names
    variable_list.update({'pivot_value_var_list':pivot_value_var_list})


    #to keeep track of whether or not we loaded a file
    loaded_file = False









#%%
    def __init__(self, parent):

        #initialize PMW module for scollable frame widget
        Pmw.initialise(parent)



        self.parent = parent
        self.df = None
        self.df_preview = None


        #create bottom frame
        bottom_frame = tk.Frame(root,name='bottom_frame')
        bottom_frame.pack(side = tk.BOTTOM)

        #add buttons
        #load
        button = tk.Button(bottom_frame, text='Load File / Restart', command=self.load)
        button.pack(side = tk.LEFT)
        #preview
        button = tk.Button(bottom_frame, text='Preview Changes', command=self.preview)
        button.pack(side = tk.LEFT)
        #export csv
        button = tk.Button(bottom_frame, text='Export to CSV', command=self.export_csv)
        button.pack(side = tk.LEFT)
        #export excel
        button = tk.Button(bottom_frame, text='Export to XLSX', command=self.export_xlsx)
        button.pack(side = tk.LEFT)
        #create a template
        button = tk.Button(bottom_frame, text='Create Template', command=self.create_template)
        button.pack(side = tk.LEFT)
        #load a template
        button = tk.Button(bottom_frame, text='Load Template', command=self.load_template)
        button.pack(side = tk.LEFT)



#will be removing if we can get the dropdown widget to work
#        self.button = tk.Button(bottom_frame, text='Move field', command=self.rearrange_field)
#        self.button.pack(side = tk.LEFT)


##used during testing - okay to delete
#        self.button = tk.Button(bottom_frame, text='Print Frame List', command=self.display_frame_list)
#        self.button.pack(side = tk.LEFT)
##used during testing
#        self.button = tk.Button(bottom_frame, text='Print Frame NAME List', command=self.display_frame_name_list)
#        self.button.pack(side = tk.LEFT)

        #scrollbar
        self.sc = Pmw.ScrolledFrame(self.parent, usehullsize=1, hull_height = 650)
        self.sc.pack(anchor = NW, fill = 'both')


#for testing
#        self.df = pd.read_csv(r'C:\Users\jpmul\Desktop\Test file.csv')



#%%
#
##used during testing
#    def display_frame_list(self):
#        print(self.frame_list)
#
#    def display_frame_name_list(self):
#        print("display_frame_name_list")
#        for frame in self.frame_list:
#            print(frame.name.get())

#%%
    def load(self):
        #start over with frames
        self.sc.destroy()
        #scrollbar
        self.sc = Pmw.ScrolledFrame(self.parent, usehullsize=1, hull_height = 650)
        self.sc.pack(anchor = NW, fill = 'both')


        #clear frame list for rebuilding
        self.frame_list.clear()


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
#%%
        if self.df is not None:
            field_list = list(self.df.columns)


            #create a new frame with each field
            for field in field_list:
                #create new frame instance, pass field name as frame name
                    #duplicate field names is going to cause issues
                my_frame = MyFrame()
                my_frame._init_(field)

                #add to list of frames so you can later iterate
                self.frame_list.append(my_frame)

                left_frame = tk.LabelFrame(self.sc.interior(),text=field,name=str(field.lower()))
                left_frame.pack(side=tk.LEFT)
                #put the name on the list of frame widgets
                self.widget_frame_list.append(str(field.lower()))


#%%
        #SORT FUNCTION
                #sort modes for radio button widget
                modes = [('Sort Ascending','A'),('Sort Descending','D'),('Do Not Sort','N')]
                for text, mode in modes:
                    b = Radiobutton(left_frame, text=text, variable=my_frame.sort_var, value=mode, indicatoron =0)
                    b.pack(side=tk.BOTTOM,anchor=W)


##            #building as a dropdown
#                modes2 = [('Do Not Sort'),('Sort Ascending'),('Sort Descending')]
#
#                rad_var = StringVar()
#                rad_var.set('Do Not Sort') # set the default option
#
#                rad_menu = OptionMenu(left_frame, rad_var, *modes2).pack(side=tk.BOTTOM)\


#%%
        #Pivot FUNCTION
                #sort modes for radio button widget
                pivot_modes = [('Pivot Row','R'),('Pivot Column','C'),('Pivot Value','V'),('Do not include in Pivot','N')]
                for text, mode in pivot_modes:
                    b = Radiobutton(left_frame, text=text, variable=my_frame.pivot_var, value=mode, indicatoron =0)
                    b.pack(side=tk.BOTTOM,anchor=W)

#%%

            #filter boxes

                filter_val = StringVar()
                filter_val.set('Filter by what?')
                filter_Entry = Entry(left_frame,textvariable=filter_val).pack(side = tk.BOTTOM)
                #change all to lowercase here or within the function to do the filtering


#%%
            #create rename box
                string_var = StringVar()
                string_var.set('Rename')
                rename_Entry = Entry(left_frame,textvariable=string_var).pack(side = tk.BOTTOM)

#%%
             #rearrange boxes

#            #building as a dropdown

                choices = list(field_list)
                choices.append('Move to End')
                choices.insert(0,'Move to Front')

                move_field_var = StringVar()
                move_field_var.set('Move Field After...') # set the default option

                move_field_menu = OptionMenu(left_frame, move_field_var, *choices).pack(side=tk.BOTTOM)
##                Label(mainframe, text="Choose a dish").grid(row = 1, column = 1)


#             #for the current field, get the contents in a df
#             new_order = field_order.copy()
#             new_order.remove(field_name)
#             new_order.insert(new_order.index(second_field) + 1, first_field)
#             self.df = self.df.replace(new_order)


#%%
            #create delete box
                int_var = IntVar()
                delete_checkbutton = Checkbutton(left_frame, text='Delete', variable=int_var).pack(side = tk.BOTTOM)




#%%

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



#%%
    def create_var_lists(self):

        #clear the variable lists
        self.sort_var_list.clear()
        self.pivot_col_var_list.clear()
        self.pivot_row_var_list.clear()
        self.pivot_value_var_list.clear()



        #loop through frames to create variable list
        for frame in self.frame_list:

#get frame name
            frame_name = frame.name.get()


#sort function
            sort_var = frame.sort_var.get()
            self.sort_var_list.update({frame_name:sort_var})

#pivot function
            #get the pivot variable for that frame
            cur_pivot_var = frame.pivot_var.get()

            #add to the respective list of columns, as applicable
            #this way, we have 3 separate lists of column (frame) names
                #which will be put into the pivot function
            if cur_pivot_var == "R":
                self.pivot_row_var_list.append(frame_name)
            elif cur_pivot_var == "C":
                self.pivot_col_var_list.append(frame_name)
            elif cur_pivot_var == "V":
                self.pivot_value_var_list.append(frame_name)




#delete

#rename

#filter



#        print(self.sort_var_list)

#%%
    def preview(self):

        #first, create all the variable lists
        if self.loaded_file == False:
            self.create_var_lists()
        else:
            #reset loaded file to false so you can make edits and still preview
            self.loaded_file = False
            #assigning the MyClass variables from the loaded list
            #all variables need to be listed here
            self.pivot_col_var_list = self.variable_list.get('pivot_col_var_list')
            self.pivot_row_var_list = self.variable_list.get('pivot_row_var_list')
            self.pivot_value_var_list = self.variable_list.get('pivot_value_var_list')
            self.sort_var_list = self.variable_list.get('sort_var_list')
            #add in remaining variables for other functions



        #(re-)set preview df to original df
        self.df_preview = self.df


        #go through each function
        self.sort_field()
        self.pivot()

        #add all other functions
        #delete
        #rename
        #etc.



        #print out during testing
        #needs to be replaced with opening in another window or excel or something
        print('\nthis is the self.df_preview dataframe\n')
        print(self.df_preview)


        #remove after testing
        print('\nthis is the original self.df dataframe\n')
        print(self.df)



#%%
    def sort_field(self):

#        #for testing
#        print('\nthis is the sort var in the sort field function\n')
#        print(self.sort_var_list)

        #loop through the sort list
        for key in self.sort_var_list:
            sort_order = self.sort_var_list.get(key)
            if sort_order == "A":
                self.df_preview.sort_values(by=key, ascending=True,inplace=True, kind='mergesort')
            elif sort_order == "D":
                self.df_preview.sort_values(by=key, ascending=False,inplace=True, kind='mergesort')



#%%
    def create_template(self):
        #create variable lists from current settings
        self.create_var_lists()

#        print('this is the variable list as of the start of create_template\n')
#        print(self.variable_list)

        #get folder path
        #this folder will hold all the variable files for the template
        export_path = fd.askdirectory(initialdir="/", title='Select save location')



        #loop through the list of variables to dump out all variables
        #using key as the name of the file/variable


        for key in self.variable_list:

            #get the variable object from the dictionary
            value = self.variable_list[key]
            #create filename in it's entirety
            filename = export_path + "/"  + key + '.p'
            #open file for writing, and then dump
            with open(filename,'wb') as f:
                pickle.dump(value,f)


#%%
    def load_template(self):

        #change loaded_file to true, this tells preview function to act differently
        self.loaded_file = True

#        export_name = fd.askopenfilename(filetypes = [('template', ('*.p'))])
#        self.sort_var_list = pickle.load(open(export_name, "rb" ))

        #put this back in after testing
        export_path = fd.askdirectory(initialdir="/", title='Select file folder')

        #testing
#        export_path = r'C:\Users\jpmul\Desktop\template storage\test3'

        #puts all files in this folder ending in ".p" into a list
#        filenames = glob.glob(export_path + '*.p')
        filenames = glob.glob(export_path + '\*.p')



        for file in filenames:
            #trim off parts of filepath+name, to get to just the name
            pickled_variable_name = str(file[len(export_path)+1:len(file)-2])



            #using the particular filename (not the full location)
                #for each file in filenames, lookup the variable from the dictionary of variables
                #which is established upon loading the program
                #then assign that pickled variable to the matching value in the dictionary
            #the "create var lists" function will then take this list and assign the values back to
                #the MyClass variables

            self.variable_list[pickled_variable_name] = pickle.load(open(file,'rb'))


        #automatically preview
        self.preview()



#%%
    def pivot(self):

        #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            self.df_preview = pd.pivot_table(self.df, index=self.pivot_row_var_list, columns=self.pivot_col_var_list, values=self.pivot_value_var_list, dropna=False,aggfunc='count')

#%%
    def delete_field(self):
        #make sure there's a daaframe loaded, otherwise, do nothing
        if self.df is not None:
            field_name = simpledialog.askstring("Delete Field", "Field to delete?",
                                parent=self.parent)
            self.df = self.df.drop(columns = field_name)

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
    def export_csv(self):
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df_preview is not None:
            export_name = fd.asksaveasfilename(filetypes = [('CSV', '*.csv',)])
            self.df_preview.to_csv(export_name + '.csv', index=None, header=True)
        # If no dataframe has been created yet
        else:
            messagebox.showerror("Error", "No data has been loaded yet!", parent=self.parent)


#%%
    def export_xlsx(self):
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df_preview is not None:
            #open sys file dialog to save
            export_name = fd.asksaveasfilename(filetypes = [('Excel', ('*.xls', '*.xlsx'))])
            self.df_preview.to_excel(export_name + '.xlsx', index=False)

        # If no dataframe has been created yet
        else:
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

    #sort raddio button variable
        self.sort_var = StringVar()
        self.sort_var.set("N")


    #pivot raddio button variable
        self.pivot_var = StringVar()
        self.pivot_var.set("N")

        #do all the same as above for each function's variable need

        #DELETE FUNCTION

        #FILTER FUNCTION

        #RENAME FUNCTION



#%%
# --- main ---

if __name__ == '__main__':



    #create root window
    root = tk.Tk()
    root.title('Spreadhsheet Miracle Machine Demo')
    root.geometry('1000x750')

    top = MyWindow(root)


    root.mainloop()
