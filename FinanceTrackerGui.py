import tkinter as tk
from tkinter import ttk

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


label1 = tk.Label(frame1, text="Budget:", anchor="w", font=("Arial", 28), bg="lightgrey", fg="black")
label1.grid(row=0, column=0, padx=25, pady=25, sticky="w")

label2 = tk.Label(frame1, text="Funds Remaining:", anchor="w", font=("Arial", 28), bg="lightgrey", fg="black")
label2.grid(row=1, column=0, padx=25, pady=25, sticky="w")

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

button = tk.Button(root, text="Add New Expense")
button.grid(row=2, column=0, columnspan=2, pady=10)

# Start the main event loop
root.mainloop()
