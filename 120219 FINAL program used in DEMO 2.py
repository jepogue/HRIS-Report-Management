




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
    interior_frame_list = []
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

    #filter function var list
    filter_var_list = OrderedDict()
    variable_list.update({'filter_var_list':filter_var_list})


    #to keeep track of whether or not we loaded a file
    loaded_file = False

    #rename function var list
    rename_var_list = OrderedDict()
    variable_list.update({'rename_var_list':rename_var_list})

    #delete function var list
    delete_var_list = OrderedDict()
    variable_list.update({'delete_var_list':delete_var_list})

    #rearrange function var list
    swap_var_list = []
    variable_list.update({'swap_var_list':swap_var_list})


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

        self.button = tk.Button(bottom_frame, text='Move field', command=self.swap_fields)
        self.button.pack(side = tk.LEFT)

        self.button = tk.Button(bottom_frame, text='Merge two reports', command=self.merge_reports)
        self.button.pack(side = tk.LEFT)



        #scrollbar
        self.sc = Pmw.ScrolledFrame(self.parent, usehullsize=1, hull_height = 650)
        self.sc.pack(anchor = NW, fill = 'both')




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

            #instantiate the swap var list, in case it's not changed
            self.swap_var_list = field_list.copy()

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

#%%
        #Pivot FUNCTION
                #sort modes for radio button widget
                pivot_modes = [('Pivot Row','R'),('Pivot Column','C'),('Pivot Value','V'),('Do not include in Pivot','N')]
                for text, mode in pivot_modes:
                    b = Radiobutton(left_frame, text=text, variable=my_frame.pivot_var, value=mode, indicatoron =0)
                    b.pack(side=tk.BOTTOM,anchor=W)

#%%

            #filter boxes

                filter_Entry = Entry(left_frame,textvariable=my_frame.filter_var).pack(side = tk.BOTTOM)
                #change all to lowercase here or within the function to do the filtering


#%%
            #create rename box
                rename_Entry = Entry(left_frame,textvariable=my_frame.rename_var).pack(side = tk.BOTTOM)




#%%
                #create delete box
                #DELETE
                b = Checkbutton(left_frame, text='Delete', variable = my_frame.delete_var, onvalue = 'D', offvalue = 'N' )
                b.pack(side=BOTTOM, anchor = W)




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
        self.filter_var_list.clear()
        self.rename_var_list.clear()
#        self.swap_var_list.clear()

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
            #delete
            delete_var = frame.delete_var.get()
            self.delete_var_list.update({frame_name:delete_var})
#rename
            rename_var = frame.rename_var.get()
            self.rename_var_list.update({frame_name:rename_var})
#filter

            filter_var = frame.filter_var.get()
            self.filter_var_list.update({frame_name:filter_var})

#rearrange
        self.variable_list.update({'swap_var_list':self.swap_var_list})
#            self.swap_var_list = self.swap_var_list.copy()



#%%
    def preview(self):



        if self.df is not None:
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
                self.filter_var_list = self.variable_list.get('filter_var_list')
                self.rename_var_list = self.variable_list.get('rename_var_list')
                self.delete_var_list = self.variable_list.get('delete_var_list')
                self.swap_var_list = self.variable_list.get('swap_var_list')
                #add in remaining variables for other functions




#            #(re-)set preview df to original df
            self.df_preview = self.df.copy()
#

            #go through each function
            self.sort_field()

#            self.filter_field()



            self.df_preview = self.df_preview[self.swap_var_list]
#            self.delete_field()
            self.pivot()
            self.filter_field()
            self.rename_field()



            self.delete_field()


            top = Toplevel()
            top.title('Preview of Changes')
            T = tk.Text(top)
            T.pack()
            T.insert(tk.END, self.df_preview)
            button = Button(top, text="Done Previewing", command=top.destroy)
            button.pack()



#%%
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
#            if sort_order == "A":
#                self.df_preview = self.df.sort_values(by=key, ascending=True,inplace=False, kind='mergesort')
#            elif sort_order == "D":
#                self.df_preview = self.df.sort_values(by=key, ascending=False,inplace=False, kind='mergesort')

            if sort_order == "A":
                self.df_preview = self.df_preview.sort_values(by=key, ascending=True,inplace=False, kind='mergesort')
            elif sort_order == "D":
                self.df_preview = self.df_preview.sort_values(by=key, ascending=False,inplace=False, kind='mergesort')

#%%
    def create_template(self):



        #create variable lists from current settings
        self.create_var_lists()



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
            if ((self.pivot_value_var_list != []) and ((self.pivot_col_var_list != []) or (self.pivot_row_var_list != []))):
#                self.df_preview = pd.pivot_table(self.df, index=self.pivot_row_var_list, columns=self.pivot_col_var_list, values=self.pivot_value_var_list, dropna=False,aggfunc='count')
                self.df_preview = pd.pivot_table(self.df_preview, index=self.pivot_row_var_list, columns=self.pivot_col_var_list, values=self.pivot_value_var_list, dropna=False,aggfunc='count')



#%%
    def delete_field(self):

        print('\ndelete var list')
        print(self.delete_var_list)

        print('\nrename_var_list')
        print(self.rename_var_list)

        for item in self.delete_var_list:
            delete = self.delete_var_list.get(item)
#            if(item in self.df_preview.columns):
#                if(delete == 'D'):
#                    self.df_preview = self.df_preview.drop(columns = item,axis=1)

            print('\nself.df_preview.columns')
            print(self.df_preview.columns)

            print('\nitem')
            print(item)

            new_item_name = self.rename_var_list[item]

            if(new_item_name in self.df_preview.columns):
                if(delete == 'D'):
                    print('\nself.rename_var_list[item]')
                    print(self.rename_var_list[item])
                    self.df_preview = self.df_preview.drop(columns = self.rename_var_list[item],axis=1)

#%%
    def filter_field(self):


#                #loop through the sort list
        for key in self.filter_var_list:
            filter_val = self.filter_var_list.get(key)
            if ((filter_val != 'Filter by what?') and (filter_val != '')):
#                self.df_preview = self.df[self.df[key]==filter_val]
                self.df_preview = self.df_preview[self.df_preview[key]==filter_val]
#%%
    def rename_field(self):

        #need a copy so we can change the column names
#        self.rename_var_list_COPY = OrderedDict()

        #loop through the sort list
        for key in self.rename_var_list:
            rename_val = self.rename_var_list.get(key)
            if ((rename_val != 'Rename') and (rename_val != '')):
#                self.df_preview = self.df.rename(columns={key:rename_val}, inplace=False)
                self.df_preview = self.df_preview.rename(columns={key:rename_val}, inplace=False)
                #update key list for field list dictionary
                #key is the key and the rename val is the new val, so the key needs to become the val
#                self.rename_var_list_COPY[rename_val] = self.rename_var_list[key] #returns the value, puts into a new entry
#                del self.rename_var_list[key]
            else:
                #update so rename is all the same (if no change)

                self.rename_var_list[key] = key


        print(self.rename_var_list)




#%%
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
                new_list.insert(new_list.index(before_field), field_name)

                self.swap_var_list = new_list.copy()



#%%

    def merge_reports(self):
            #get filename for opening file 1

#        messagebox.showinfo("Select 1st file", "Please select your first file", parent=self.parent)
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

        df1 = self.df.copy()



#ask for file 2
#        messagebox.showinfo("Select 2nd file", "Please select your second file", parent=self.parent)
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


        df2 = self.df.copy()



        join_key = simpledialog.askstring("Merge Reports", "What is the shared key to join the reports?", parent=self.parent)


        join_type = simpledialog.askstring("Merge Reports", "Left / Right / Inner / Outer", parent=self.parent)
        join_type = join_type.lower()
        #need to do more checking here



        self.df_preview = df1.merge(df2,how = join_type, on = join_key,left_index=True, right_index=True)
#        self.df_preview = df1.merge(df2,how = join_type, on = join_key))

        #auto preview - outside of normal preview
        top = Toplevel()
        top.title('Preview of Changes')
        T = tk.Text(top)
        T.pack()
        T.insert(tk.END, self.df_preview)
        button = Button(top, text="Done Previewing", command=top.destroy)
        button.pack()




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

        self.name = StringVar()
        self.name.set(field)


    #sort raddio button variable
        self.sort_var = StringVar()
        self.sort_var.set("N")


    #pivot raddio button variable
        self.pivot_var = StringVar()
        self.pivot_var.set("N")

        #do all the same as above for each function's variable need

        #DELETE FUNCTION
        self.delete_var = StringVar()
        self.delete_var.set('N')



        #FILTER FUNCTION
        self.filter_var = StringVar()
        self.filter_var.set('Filter by what?')

        #RENAME FUNCTION
        self.rename_var = StringVar()
        self.rename_var.set('Rename')



#%%
# --- main ---

if __name__ == '__main__':



    #create root window
    root = tk.Tk()
    root.title('Spreadhsheet Miracle Machine Demo')
    root.geometry('1000x750')

    top = MyWindow(root)


    root.mainloop()
