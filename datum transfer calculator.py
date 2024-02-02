#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing necessary packages
import pandas as pd
import numpy as np  
import tkinter as tk
from tkinter import filedialog, ttk
import os, sys
import time


# In[2]:


#function to get needed columns from the low water data
def get_low(data):

    n = 0
    q = 4
    l =[]
    for i in range(len(data)):
        
        if i % 4 == 0:
            
            l.append(data[n:q]) 
            n+=4
            q+=4   
    return l


#function to get needed columns from the high water data

def get_high(data_h):
    indices_to_remove = list(range(3, len(data_h), 4))
    
    # Create a boolean mask to filter out elements to be removed
    mask = np.ones(len(data_h), dtype=bool)
    mask[indices_to_remove] = False
    
    # Apply the mask to get the desired elements
    data_h = data_h[mask]
   

    n= 0
    q = 3
    l =[]
    for i in range(len(data_h)):
        if i % 3 == 0:            
            l.append(data_h[n:q]) 
            n+=3
            q+=3

    return l



#Function to calculate Mean High Water, Mean Low Water, Range, and Mean Tide Level for df_1
def equation_1(low, high):
    r = []
    m = []
    for i in range(15):
        a,c,e,g = low[i]
        b,d,f = high[i]
        MLW = (a+ 3*c+ 3*e + g )/8
        MHW = (b+ 2*d + f)/4
        r.append(MHW - MLW)
        m.append((MHW + MLW) / 2)

    return r,m

#Function to calculate Mean High Water, Mean Low Water, Range, and Mean Tide Level for df_2
def equation_2(low_2, high_2):
    R = []
    M_ = []
    for i in range(15):
        a,c,e,g = low_2[i]
        b,d,f = high_2[i]
        MLW = (a+ 3*c+ 3*e + g )/8
        MHW = (b+ 2*d + f)/4
        R.append(MHW - MLW)
        M_.append((MHW + MLW) / 2)

    return R,M_

def sound_datum(r,m, R, M_):
    d = []
    for i in range(15):
        M = 0.518       
        d.append((m[i] -(M_[i] - M)-(M*r[i]/R[i])))
    return d



# In[3]:


def operation_trigger(file1_path, file2_path):
    """
        Function to trigger the get low, get high and sound datum 
        after reading the data in the uploaded files.
    """
    df_1 = pd.read_csv(file1_path)
    df_2 = pd.read_csv(file2_path)

    try:
        low_1 = get_low(df_1['LW'])
    except:
        tk.messagebox.showwarning("Error", "Please, make sure low water column is in file 1.")

    try:
        low_2 = get_low(df_2['LW']) 
    except:
        tk.messagebox.showwarning("Error", "Please, make sure low water column is in file 2.")

    try:
        high_1 = get_high(df_1['HW'])
    except:
        tk.messagebox.showwarning("Error", "Please, make sure high water column is in file 1.")

    try:
        high_2 = get_high(df_2['HW'])
    except:
        tk.messagebox.showwarning("Error", "Please, make sure high water column is in file 2.")
 

    r, m = equation_1(low_1, high_1)   
    R, M_ = equation_2(low_2, high_2)

    new_gauge_sounding_datum = sound_datum(r,m,R,M_)

    new_gauge_sounding_datum = [round(i,2) for i in new_gauge_sounding_datum]

    return new_gauge_sounding_datum, r, m, R, M_

def browse_file(entry_widget):
    """
        Function to browse files on the system to be uploaded, 
        restricting to only CSV files.
    """
    file_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def execute_operation(file1_path, file2_path, root):
    """
        Function responsible for displaying a preview 
        after computing before saving to file on a system.
    """
    new_gauge_sounding_datum, r, m, R, M_ = operation_trigger(file1_path, file2_path)
    
    results = pd.DataFrame({ 
                      'Tidal Range at Secondary Port (m)': r, 
                      'MTL_Secondary (m)': m,
                      'Tidal Range at Established Gauge/Port (m)':R,
                      'MTL_Established (m)':M_,
                      'New Gauge Sounding Datum (m)': new_gauge_sounding_datum}
                      )    #converting to a pandas Dataframe
    result_dialog = tk.Toplevel(root)
    result_dialog.title("New Gauge Sounding Datum")
    # result_label = tk.Label(result_dialog, text="New Sounding Datum:\n" + str(results))
    # result_label.pack()
    tree = ttk.Treeview(result_dialog, columns=results.columns, show="headings")
    num = 0
    for col in results.columns:
        tree.heading(num, text=col)
        num+=1

    for index, row in results.iterrows():
        values = [str(row[col]) for col in results.columns]
        tree.insert("", "end", values=values)

    tree.pack(expand=True, fill="both")
    save_button = tk.Button(result_dialog, text="Save Result as CSV", command=lambda: save_result_csv(results))
    save_button.pack()

def save_result_csv(results):
    """
        Function to save computing result to file on a system.
    """
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    results.to_csv(save_path, index=False)  # saves to a csv file
    tk.messagebox.showinfo("Show Successful", "Result saved successfully as CSV.")

def on_execute_button(entry_file1, entry_file2, root):
    """
        Function to trigger getting of files from the system.
    """
    file1_path = entry_file1.get()
    file2_path = entry_file2.get()

    if file1_path and file2_path:
        execute_operation(file1_path, file2_path, root)
    else:
        tk.messagebox.showwarning("Error", "Please. select both CSV files.")


# In[6]:


root = tk.Tk()
root.title("Datum Transfer Calculator")

label_file1 = tk.Label(root, text="Select Secondary Port:")
label_file1.grid(row=0, column=0, padx=10, pady=10)
entry_file1 = tk.Entry(root, width=50)
entry_file1.grid(row=0, column=1, padx=10, pady=10)
browse_button_file1 = tk.Button(root, text="Browse", command=lambda: browse_file(entry_file1))
browse_button_file1.grid(row=0, column=2, padx=10, pady=10)

label_file2 = tk.Label(root, text="Select Standard Port:")
label_file2.grid(row=1, column=0, padx=10, pady=10)
entry_file2 = tk.Entry(root, width=50)
entry_file2.grid(row=1, column=1, padx=10, pady=10)
browse_button_file2 = tk.Button(root, text="Browse", command=lambda: browse_file(entry_file2))
browse_button_file2.grid(row=1, column=2, padx=10, pady=10)

execute_button = tk.Button(root, text="Run", command=lambda: on_execute_button(entry_file1, entry_file2, root))
execute_button.grid(row=2, column=1, pady=20)

owner_info = tk.Label(root, text="Datum Transfer Calculator by Group 1", font=("Calibri", 14, "bold"), fg="black")
owner_info.grid(row=3, column=0, columnspan=3)

root.mainloop()


# In[ ]:




