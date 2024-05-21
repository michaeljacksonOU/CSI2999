import tkinter as tk
from tkinter import ttk

def budget_window():

    # Create the budget window
    global budget_window
    budget_window = tk.Tk()
    budget_window.title("Monthly Budget")
    budget_window.geometry("600x600")
    
    label1 = tk.Label(budget_window, text="Enter your monthly budget:")
    label1.pack()
    
    budget_amount = tk.Entry(budget_window)
    budget_amount.pack()
    
    # Create the confirm_button
    # When the Confirm button is clicked, the close_budget_window() method is called and the budget is sent to that method
    confirm_button = tk.Button(budget_window, text="Confirm", command=lambda: close_budget_window(budget_amount.get()))
    confirm_button.pack(padx=10, pady=10)
   
    # Start the budget event loop
    budget_window.mainloop()

# End method budget_window()

# The budget is received as a parameter from the budget_window method
def close_budget_window(budget):
    # Close the budget window
    budget_window.destroy()

    # Open the main window and send the budget to that method
    main_window(budget)

# End method close_budget_window()    

def main_window(budget):

    # Create the main window
    root = tk.Tk()
    root.title("Budget Tracker")
    root.geometry("600x600")

    # Create four frames
    frame1 = tk.Frame(root, bg="lightgrey", width=250, height=250)
    frame2 = tk.Frame(root, bg="lightgrey", width=250, height=250)
    frame3 = tk.Frame(root, bg="lightgrey", width=250, height=250)
    frame4 = tk.Frame(root, bg="lightgrey", width=250, height=250)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    frame1.grid_propagate(False)
    frame2.grid_propagate(False)
    frame3.grid_propagate(False)
    frame4.grid_propagate(False)

    # Convert the budget amount to a float
    budget_amount = float(budget)

    # Create budget and funds labels
    label1 = tk.Label(frame1, text="Budget:", anchor="w", font=("Arial", 28), bg="lightgrey", fg="black")
    label1.grid(row=0, column=0, padx=25, pady=25, sticky="w")
    
    budget_amount_label = tk.Label(frame1, text="${:,.2f}".format(budget_amount), anchor="w", font=("Arial", 28), bg="lightgrey", fg="black")
    budget_amount_label.grid(row=0, column=1, padx=25, pady=25, sticky="w")

    label2 = tk.Label(frame1, text="Funds Remaining:", anchor="w", font=("Arial", 28), bg="lightgrey", fg="black")
    label2.grid(row=1, column=0, padx=25, pady=25, sticky="w")

    funds_remaining_label = tk.Label(frame1, text="${:,.2f}".format(budget_amount), anchor="w", font=("Arial", 28), bg="lightgrey", fg="black")
    funds_remaining_label.grid(row=1, column=1, padx=25, pady=25, sticky="w")

    tree = ttk.Treeview(frame2, show="headings")

    tree["columns"] = ("Name", "Type", "Price", "Date")

    tree.column("Name", width=100, anchor="w", stretch=tk.YES)
    tree.column("Type", width=100, anchor="w", stretch=tk.YES)
    tree.column("Price", width=100, anchor="w", stretch=tk.YES)
    tree.column("Date", width=100, anchor="w", stretch=tk.YES)

    tree.heading("Name", text="Name", anchor="w")
    tree.heading("Type", text="Type", anchor="w")
    tree.heading("Price", text="Price", anchor="w")
    tree.heading("Date", text="Date", anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")

    frame2.grid_rowconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)
    frame2.grid_columnconfigure(1, weight=0)


    # Place the frames in a 2x2 grid
    frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    frame3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    frame4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # Create Add New Expense button
    add_new_expense_button = tk.Button(root, text="Add New Expense")
    add_new_expense_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Start the main event loop
    root.mainloop()

# End method main_window()

# Call to method budget_window() that will start the program
budget_window()
