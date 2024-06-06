import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np

def normalize(column, criteria_type='MAX'):
    if criteria_type == 'MAX':
        return (column - column.min()) / (column.max() - column.min())
    elif criteria_type == 'MIN':
        return (column.max() - column) / (column.max() - column.min())

def calculate_custom_correlation(df):
    n = len(df.columns)
    correlation_matrix = np.zeros((n, n))  # Initialize with zeros

    for i in range(n):
        for j in range(n):
            if i != j:
                col_i = df.columns[i]
                col_j = df.columns[j]
                correlation_matrix[i, j] = 1 - df[col_i].corr(df[col_j])

    return pd.DataFrame(correlation_matrix, index=df.columns, columns=df.columns)

def calculate_criteria_weights(data, criteria_types):
    df = pd.DataFrame(data)
    
    # Apply normalization
    normalized_df = df.copy()
    for criteria, criteria_type in criteria_types.items():
        normalized_df[criteria] = normalize(df[criteria], criteria_type)
    
    # Drop 'Alternative' column for correlation calculation
    normalized_df_no_alt = normalized_df.drop(columns=['Alternative'])
    
    # Calculate correlation with the given logic
    custom_correlation_matrix = calculate_custom_correlation(normalized_df_no_alt)
    
    # Calculate standard deviation for each criterion
    std_devs = normalized_df_no_alt.std()
    
    # Calculate information content for each criterion
    info_content = std_devs * custom_correlation_matrix.sum(axis=1)
    
    # Calculate weights for each criterion
    weights = info_content / info_content.sum()
    
    return normalized_df, custom_correlation_matrix, weights

def create_treeview(parent, dataframe):
    container = ttk.Frame(parent)
    container.pack(expand=True, fill='both')
    
    tree = ttk.Treeview(container, show='headings')
    tree["columns"] = list(dataframe.columns)
    for col in dataframe.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')
    for index, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))
    
    h_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
    v_scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    
    tree.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
    
    tree.grid(row=0, column=0, sticky='nsew')
    v_scrollbar.grid(row=0, column=1, sticky='ns')
    h_scrollbar.grid(row=1, column=0, sticky='ew')
    
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

def on_calculate():
    try:
        # Read data from entry widgets
        data = {
            'Alternative': ['Fitness and Health', 'Fun and Games', 'Education and Learning', 'Industrial and Workplace', 'Fashion and Style'],
            'Accuracy and Precision': [float(entry_criteria1_a1.get()), float(entry_criteria1_a2.get()), float(entry_criteria1_a3.get()), float(entry_criteria1_a4.get()), float(entry_criteria1_a5.get())],
            'Privacy and Security': [float(entry_criteria2_a1.get()), float(entry_criteria2_a2.get()), float(entry_criteria2_a3.get()), float(entry_criteria2_a4.get()), float(entry_criteria2_a5.get())],
            'Performance': [float(entry_criteria3_a1.get()), float(entry_criteria3_a2.get()), float(entry_criteria3_a3.get()), float(entry_criteria3_a4.get()), float(entry_criteria3_a5.get())],
            'Battery Drainage': [float(entry_criteria4_a1.get()), float(entry_criteria4_a2.get()), float(entry_criteria4_a3.get()), float(entry_criteria4_a4.get()), float(entry_criteria4_a5.get())],
            'UI x UX': [float(entry_criteria5_a1.get()), float(entry_criteria5_a2.get()), float(entry_criteria5_a3.get()), float(entry_criteria5_a4.get()), float(entry_criteria5_a5.get())],
            'Connection and Sync': [float(entry_criteria6_a1.get()), float(entry_criteria6_a2.get()), float(entry_criteria6_a3.get()), float(entry_criteria6_a4.get()), float(entry_criteria6_a5.get())],
            'Ease of Use': [float(entry_criteria7_a1.get()), float(entry_criteria7_a2.get()), float(entry_criteria7_a3.get()), float(entry_criteria7_a4.get()), float(entry_criteria7_a5.get())],
            'Future Updates': [float(entry_criteria8_a1.get()), float(entry_criteria8_a2.get()), float(entry_criteria8_a3.get()), float(entry_criteria8_a4.get()), float(entry_criteria8_a5.get())],
            'Personalization': [float(entry_criteria9_a1.get()), float(entry_criteria9_a2.get()), float(entry_criteria9_a3.get()), float(entry_criteria9_a4.get()), float(entry_criteria9_a5.get())],
            'Interactivity': [float(entry_criteria10_a1.get()), float(entry_criteria10_a2.get()), float(entry_criteria10_a3.get()), float(entry_criteria10_a4.get()), float(entry_criteria10_a5.get())],
            'Language Support': [float(entry_criteria11_a1.get()), float(entry_criteria11_a2.get()), float(entry_criteria11_a3.get()), float(entry_criteria11_a4.get()), float(entry_criteria11_a5.get())],
            'Diversity and Scope of Functions': [float(entry_criteria12_a1.get()), float(entry_criteria12_a2.get()), float(entry_criteria12_a3.get()), float(entry_criteria12_a4.get()), float(entry_criteria12_a5.get())],
            'Radiation': [float(entry_criteria13_a1.get()), float(entry_criteria13_a2.get()), float(entry_criteria13_a3.get()), float(entry_criteria13_a4.get()), float(entry_criteria13_a5.get())],
            'Cost': [float(entry_criteria14_a1.get()), float(entry_criteria14_a2.get()), float(entry_criteria14_a3.get()), float(entry_criteria14_a4.get()), float(entry_criteria14_a5.get())],
            'Design and Visual Aesthetics': [float(entry_criteria15_a1.get()), float(entry_criteria15_a2.get()), float(entry_criteria15_a3.get()), float(entry_criteria15_a4.get()), float(entry_criteria15_a5.get())]
        }
        
        criteria_types = {
            'Accuracy and Precision': var_criteria1.get(),
            'Privacy and Security': var_criteria2.get(),
            'Performance': var_criteria3.get(),
            'Battery Drainage': var_criteria4.get(),
            'UI x UX': var_criteria5.get(),
            'Connection and Sync': var_criteria6.get(),
            'Ease of Use': var_criteria7.get(),
            'Future Updates': var_criteria8.get(),
            'Personalization': var_criteria9.get(),
            'Interactivity': var_criteria10.get(),
            'Language Support': var_criteria11.get(),
            'Diversity and Scope of Functions': var_criteria12.get(),
            'Radiation': var_criteria13.get(),
            'Cost': var_criteria14.get(),
            'Design and Visual Aesthetics': var_criteria15.get()
        }
        
        normalized_df, custom_correlation_matrix, weights = calculate_criteria_weights(data, criteria_types)

        # Yuvarlama işlemi
        normalized_df = normalized_df.round(4)
        custom_correlation_matrix = custom_correlation_matrix.round(4)
        weights = weights.round(4)
        
        # Display results in a new window with tabs
        result_window = tk.Toplevel(root)
        result_window.title("Results")

        tab_control = ttk.Notebook(result_window)
        
        tab_normalized = ttk.Frame(tab_control)
        tab_correlation = ttk.Frame(tab_control)
        tab_weights = ttk.Frame(tab_control)
        
        tab_control.add(tab_normalized, text="Normalized Data")
        tab_control.add(tab_correlation, text="Correlation Matrix")
        tab_control.add(tab_weights, text="Weights")
        
        tab_control.pack(expand=1, fill='both')
        
        create_treeview(tab_normalized, normalized_df)
        create_treeview(tab_correlation, custom_correlation_matrix)
        
        weights_df = pd.DataFrame(weights, columns=['Weight'])
        create_treeview(tab_weights, weights_df)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Decision Making Tool")

# Create entry widgets for Alternatives and Criteria
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Add labels for alternatives
label_alternatives = ttk.Label(frame, text="Alternatives: Fitness and Health, Fun and Games, Education and Learning, Industrial and Workplace, Fashion and Style")
label_alternatives.grid(row=0, column=0, columnspan=7, pady=(0, 10))

# Define the function to create criteria entry rows
def create_criteria_entry(frame, row, criteria_name):
    label = ttk.Label(frame, text=criteria_name)
    label.grid(row=row, column=0, padx=5, pady=5)
    
    entry1 = ttk.Entry(frame, width=10)
    entry1.grid(row=row, column=1, padx=5, pady=5)
    
    entry2 = ttk.Entry(frame, width=10)
    entry2.grid(row=row, column=2, padx=5, pady=5)
    
    entry3 = ttk.Entry(frame, width=10)
    entry3.grid(row=row, column=3, padx=5, pady=5)
    
    entry4 = ttk.Entry(frame, width=10)
    entry4.grid(row=row, column=4, padx=5, pady=5)
    
    entry5 = ttk.Entry(frame, width=10)
    entry5.grid(row=row, column=5, padx=5, pady=5)
    
    var = tk.StringVar()
    var.set("MAX")
    combobox = ttk.Combobox(frame, textvariable=var, values=["MAX", "MIN"], state="readonly", width=5)
    combobox.grid(row=row, column=6, padx=5, pady=5)
    
    return (entry1, entry2, entry3, entry4, entry5), var

# Create entries for all 15 criteria
criteria_names = [
    "Accuracy and Precision",
    "Privacy and Security",
    "Performance",
    "Battery Drainage",
    "UI x UX",
    "Connection and Sync",
    "Ease of Use",
    "Future Updates",
    "Personalization",
    "Interactivity",
    "Language Support",
    "Diversity and Scope of Functions",
    "Radiation",
    "Cost",
    "Design and Visual Aesthetics"
]

criteria_entries = []
criteria_vars = []

for i, criteria_name in enumerate(criteria_names, start=1):
    entries, var = create_criteria_entry(frame, i, criteria_name)
    criteria_entries.append(entries)
    criteria_vars.append(var)

# Assign entries and variables to specific criteria
(entry_criteria1_a1, entry_criteria1_a2, entry_criteria1_a3, entry_criteria1_a4, entry_criteria1_a5), var_criteria1 = criteria_entries[0], criteria_vars[0]
(entry_criteria2_a1, entry_criteria2_a2, entry_criteria2_a3, entry_criteria2_a4, entry_criteria2_a5), var_criteria2 = criteria_entries[1], criteria_vars[1]
(entry_criteria3_a1, entry_criteria3_a2, entry_criteria3_a3, entry_criteria3_a4, entry_criteria3_a5), var_criteria3 = criteria_entries[2], criteria_vars[2]
(entry_criteria4_a1, entry_criteria4_a2, entry_criteria4_a3, entry_criteria4_a4, entry_criteria4_a5), var_criteria4 = criteria_entries[3], criteria_vars[3]
(entry_criteria5_a1, entry_criteria5_a2, entry_criteria5_a3, entry_criteria5_a4, entry_criteria5_a5), var_criteria5 = criteria_entries[4], criteria_vars[4]
(entry_criteria6_a1, entry_criteria6_a2, entry_criteria6_a3, entry_criteria6_a4, entry_criteria6_a5), var_criteria6 = criteria_entries[5], criteria_vars[5]
(entry_criteria7_a1, entry_criteria7_a2, entry_criteria7_a3, entry_criteria7_a4, entry_criteria7_a5), var_criteria7 = criteria_entries[6], criteria_vars[6]
(entry_criteria8_a1, entry_criteria8_a2, entry_criteria8_a3, entry_criteria8_a4, entry_criteria8_a5), var_criteria8 = criteria_entries[7], criteria_vars[7]
(entry_criteria9_a1, entry_criteria9_a2, entry_criteria9_a3, entry_criteria9_a4, entry_criteria9_a5), var_criteria9 = criteria_entries[8], criteria_vars[8]
(entry_criteria10_a1, entry_criteria10_a2, entry_criteria10_a3, entry_criteria10_a4, entry_criteria10_a5), var_criteria10 = criteria_entries[9], criteria_vars[9]
(entry_criteria11_a1, entry_criteria11_a2, entry_criteria11_a3, entry_criteria11_a4, entry_criteria11_a5), var_criteria11 = criteria_entries[10], criteria_vars[10]
(entry_criteria12_a1, entry_criteria12_a2, entry_criteria12_a3, entry_criteria12_a4, entry_criteria12_a5), var_criteria12 = criteria_entries[11], criteria_vars[11]
(entry_criteria13_a1, entry_criteria13_a2, entry_criteria13_a3, entry_criteria13_a4, entry_criteria13_a5), var_criteria13 = criteria_entries[12], criteria_vars[12]
(entry_criteria14_a1, entry_criteria14_a2, entry_criteria14_a3, entry_criteria14_a4, entry_criteria14_a5), var_criteria14 = criteria_entries[13], criteria_vars[13]
(entry_criteria15_a1, entry_criteria15_a2, entry_criteria15_a3, entry_criteria15_a4, entry_criteria15_a5), var_criteria15 = criteria_entries[14], criteria_vars[14]

# Calculate button
button_calculate = ttk.Button(root, text="Calculate", command=on_calculate)
button_calculate.pack(pady=10)

# Run the application
root.mainloop()
