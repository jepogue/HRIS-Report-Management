

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
    filename = None
    sort_var_list = OrderedDict()
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
        button = tk.Button(bottom_frame, text='Load File / Restart', command=self.load)
        button.pack(side = tk.LEFT)

#don't need this - user will just click on "load" when they want to restart
#        button = tk.Button(bottom_frame, text='Revert to Original', command=self.load)
#        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Preview Changes', command=self.preview)
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Export to CSV', command=self.export_csv)
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Export to XLSX', command=self.export_xlsx)
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Create Template', command=self.create_template)
        button.pack(side = tk.LEFT)

        button = tk.Button(bottom_frame, text='Load Template', command=self.load_template)
        button.pack(side = tk.LEFT)




#        self.button = tk.Button(bottom_frame, text='Move field', command=self.rearrange_field)
#        self.button.pack(side = tk.LEFT)


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

                #master=self.parent is causing it to be in botton of frame
                left_frame = tk.LabelFrame(self.sc.interior(),text=field)
                left_frame.pack(side=tk.LEFT)


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
#                rad_menu = OptionMenu(left_frame, rad_var, *modes2).pack(side=tk.BOTTOM)

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

#
#            #create groupby box
#
#                group_val = StringVar()
#                group_val.set('Field to Group by')
#                filter_Entry = Entry(left_frame,textvariable=group_val).pack(side = tk.BOTTOM)
#
#    #             #for the current field, get the contents in a df
#    #             self.df = self.df.groupby(group_val).count()

#%%
#            #create pivot box
#
#                index_chosen = StringVar()
#                index_chosen.set('Rows to Pivot')
#                index_Entry = Entry(left_frame,textvariable=index_chosen).pack(side = tk.BOTTOM)
#                column_chosen = StringVar()
#                column_chosen.set('Columns to Pivot')
#                column_Entry = Entry(left_frame,textvariable=column_chosen).pack(side = tk.BOTTOM)
#                pivot_val = StringVar()
#                pivot_val.set('Pivot by what values?')
#                pivot_Entry = Entry(left_frame,textvariable=pivot_val).pack(side = tk.BOTTOM)
#
#    #            self.df = pd.pivot_table(self.df, index=index_chosen, columns=column_chosen, values = pivot_val,
#    #                                     dropna=False,aggfunc='count')




#%%
            #create delete box
                int_var = IntVar()
                delete_checkbutton = Checkbutton(left_frame, text='Delete', variable=int_var).pack(side = tk.BOTTOM)




#%%

##                left_frame = tk.LabelFrame(self.sc.interior(),text=field)
#
#                top_frame = tk.LabelFrame(left_frame.sc.interior(),text=field)
#                top_frame.pack(side=tk.TOP)
#
#                self.text = tk.Text(top_frame,width=20, height = 17).pack(side=tk.TOP)
#
#                col_df = self.df[field]
#
#                self.text.insert('end', str(col_df) + '\n')


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

        #loop through frames to create variable list
        for frame in self.frame_list:

            #sort function
            frame_name = frame.name.get()
            sort_var = frame.sort_var.get()
            self.sort_var_list.update({frame_name:sort_var})

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

        #go through each function
        self.sort_field()

        #print out during testing
        print(self.df)


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
        export_name = fd.asksaveasfilename(filetypes = [('template', ('*.p'))])
        pickle.dump(self.sort_var_list, open(export_name + ".p", "wb" ) )


#%%
    def load_template(self):

        #need to put in open dialogue prompt after testing
        #and we'll need to loop through all variable lists
        self.loaded_file = True
        export_name = fd.askopenfilename(filetypes = [('template', ('*.p'))])
        self.sort_var_list = pickle.load(open(export_name, "rb" ))
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
        if self.df is not None:
            export_name = fd.asksaveasfilename(filetypes = [('CSV', '*.csv',)])
            self.df.to_csv(export_name + '.csv', index=None, header=True)
        # If no dataframe has been created yet
        else:
            messagebox.showerror("Error", "No data has been loaded yet!", parent=self.parent)


#%%
    def export_xlsx(self):
        #make sure there's a dataframe loaded, otherwise, do nothing
        if self.df is not None:
            #open sys file dialog to save
            export_name = fd.asksaveasfilename(filetypes = [('Excel', ('*.xls', '*.xlsx'))])
            self.df.to_excel(export_name + '.xlsx', index=False)

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

        self.sort_var = StringVar()
        self.sort_var.set("N")

        #do all the same as above for each function's variable need

        #DELETE FUNCTION

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
