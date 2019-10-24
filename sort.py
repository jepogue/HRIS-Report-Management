import pandas as pd

#I'm assuming this value will be passed from the main code depending if the user wants ascending or descending sort(GUI just showing two boxes and the user clicks the one they want)
ascending_value = False
file = "test.xlsx"

#read from the file if this is already done it can be passed from the main code as a DataFrame
try:
    data = pd.read_excel(file)
except Exception:
    data = pd.read_csv(file)
#This input I am assuming will also be passed from the main code (a box for text input under sort tab in GUI)
#Ask for list from user
input_list = input("Input the headers of the columns you want sorted in the order they should be sorted seperated with commas: ")
#Get list seperated with commas
list_sort = input_list.split(",")

#Sort Values in ascending or descending order 
data.sort_values(by=list_sort, axis=0, ascending = ascending_value, inplace=True) 

#Just to show the state of the DataFrame after sort
print(data)


#Saves sorted data to excel sheet
#data.to_excel('result.xlsx')

#Saves sorted data to csv
#data.to_csv('result.csv')
