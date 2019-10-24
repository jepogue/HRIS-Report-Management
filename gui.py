import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')

# ------ Menu Definition ------ #
menu_def = [
             ['File', ['Open', 'Export to PDF', 'Email', 'Exit']],
             ['Edit', ['Rename Column', 'Delete Column', 'Rearrange Columns']],
             ['Sort'],
             ['Search'],
             ['Visualization']
           ]

layout = [
            [sg.Menu(menu_def, visible=True)],
            [sg.Text('Spreadsheet Reformatting Tool', size=(30, 1), justification='center',
             font=("Helvetica", 25))],
            [sg.Text('To begin, please import a CSV or XLS file.', size=(42, 1), justification='right',
             font=("Helvetica", 14))],
            [sg.Text('Choose A Folder', size=(35, 1))],
            [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
             sg.InputText('Default Folder'), sg.FolderBrowse()],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]
         ]

window = sg.Window('Group 1 – CSCI441 Fall 2019', layout, default_element_size=(40, 1), grab_anywhere=False)
event, values = window.Read()
