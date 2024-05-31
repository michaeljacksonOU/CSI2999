import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def budget_window():
    global funds_remaining, budget_window

    # Initialize the Tkinter window
    budget_window = tk.Tk()
    budget_window.title("Monthly Budget")
    budget_window.geometry("1920x1080")

    # Load the image
    image = Image.open("GRADIENT-BLUE.png")
    photo = ImageTk.PhotoImage(image)

    # Create a Canvas widget to hold the image
    canvas = tk.Canvas(budget_window, width=1920, height=1080)
    canvas.pack(fill="both", expand=True)

    # Display the image on the canvas
    canvas.create_image(0, 0, image=photo, anchor="nw")

    # Add widgets on top of the canvas
    label1 = tk.Label(budget_window, text="Enter your monthly budget:", font=("Arial", 20), bg="lightblue")
    canvas.create_window(960, 200, window=label1)

    budget_amount = tk.Entry(budget_window, font=("Arial", 20))
    canvas.create_window(960, 250, window=budget_amount)

    # Create the Confirm button
    confirm_button = tk.Button(budget_window, text="Confirm", command=lambda: close_budget_window(budget_amount.get()),
                               font=("Arial", 20))
    canvas.create_window(960, 300, window=confirm_button)

    # Keep a reference to the image to prevent it from being garbage collected
    budget_window.photo = photo

    # Start the budget event loop
    budget_window.mainloop()


def close_budget_window(budget):
    global funds_remaining
    # Close the budget window
    budget_window.destroy()

    funds_remaining = float(budget)

    # Open the main window and send the budget to that method
    main_window(budget)


def main_window(budget):
    # Create the main window
    root = tk.Tk()
    root.title("Budget Tracker")
    root.geometry("1920x1080")

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

    budget_amount_label = tk.Label(frame1, text="${:,.2f}".format(budget_amount), anchor="w", font=("Arial", 28),
                                   bg="lightgrey", fg="black")
    budget_amount_label.grid(row=0, column=1, padx=25, pady=25, sticky="w")

    label2 = tk.Label(frame1, text="Funds Remaining:", anchor="w", font=("Arial", 28), bg="lightgrey", fg="black")
    label2.grid(row=1, column=0, padx=25, pady=25, sticky="w")

    global funds_remaining_label
    funds_remaining_label = tk.Label(frame1, text="${:,.2f}".format(budget_amount), anchor="w", font=("Arial", 28),
                                     bg="lightgrey", fg="black")
    funds_remaining_label.grid(row=1, column=1, padx=25, pady=25, sticky="w")

    global tree
    tree = ttk.Treeview(frame2, show="headings")

    tree["columns"] = ("Name", "Type", "Price", "Priority", "Date")

    tree.column("Name", width=100, anchor="w", stretch=tk.YES)
    tree.column("Type", width=100, anchor="w", stretch=tk.YES)
    tree.column("Price", width=100, anchor="w", stretch=tk.YES)
    tree.column("Priority", width=100, anchor="w", stretch=tk.YES)
    tree.column("Date", width=100, anchor="w", stretch=tk.YES)

    tree.heading("Name", text="Name", anchor="w")
    tree.heading("Type", text="Type", anchor="w")
    tree.heading("Price", text="Price", anchor="w")
    tree.heading("Priority", text="Priority", anchor="w")
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

    # Create Add New Expense button that will open up a pop-up window to enter/upload the expense
    add_new_expense_button = tk.Button(root, text="Add New Expense", command=expense_popup)
    add_new_expense_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Bottom left box
    global high_priority_label, medium_priority_label, low_priority_label
    high_priority_label = tk.Label(frame3, text="High priority expenses : $0", anchor="w", font=("Arial", 28),
                                   bg="lightgrey", fg="black")
    high_priority_label.grid(row=0, column=0, padx=25, pady=25, sticky="w")

    medium_priority_label = tk.Label(frame3, text="Medium priority expenses : $0", anchor="w", font=("Arial", 28),
                                     bg="lightgrey", fg="black")
    medium_priority_label.grid(row=1, column=0, padx=25, pady=25, sticky="w")

    low_priority_label = tk.Label(frame3, text="Low priority expenses : $0", anchor="w", font=("Arial", 28),
                                  bg="lightgrey", fg="black")
    low_priority_label.grid(row=2, column=0, padx=25, pady=25, sticky="w")

    # Bottom right box
    style = ttk.Style()
    style.configure("TNotebook.Tab", font=('Helvetica', 25, 'bold'), padding=[40, 0])
    notebook = ttk.Notebook(frame4, style="TNotebook")

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)
    notebook.add(tab1, text="High")
    notebook.add(tab2, text="Medium")
    notebook.add(tab3, text="Low")
    notebook.pack(expand=1, fill='both')

    # Start the main event loop
    root.mainloop()


def expense_popup():
    global expense_window
    # Create the pop-up window
    expense_window = tk.Toplevel()
    expense_window.title("Add New Expense")
    expense_window.geometry("400x300")

    # Enter Manually button to allow the user to input their expense
    manual_button = tk.Button(expense_window, text="Enter Manually", command=close_expense_popup)
    manual_button.pack(pady=10)

    # Upload Receipt button to allow the user to upload their receipt from their computer files
    upload_button = tk.Button(expense_window, text="Upload Receipt")
    upload_button.pack(pady=10)


def close_expense_popup():
    expense_window.destroy()
    enter_manually_popup()


def enter_manually_popup():
    # Create the pop-up window
    enter_manually_popup = tk.Toplevel()
    enter_manually_popup.title("Manual Expense Entry")
    enter_manually_popup.geometry("800x150")

    # Create the labels
    name_label = tk.Label(enter_manually_popup, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    price_label = tk.Label(enter_manually_popup, text="Price:")
    price_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    category_label = tk.Label(enter_manually_popup, text="Category:")
    category_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")

    priority_label = tk.Label(enter_manually_popup, text="Priority:")
    priority_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")

    date_label = tk.Label(enter_manually_popup, text="Date:")
    date_label.grid(row=0, column=5, padx=10, pady=10, sticky="w")

    # Create the entry text fields
    name_entry = tk.Entry(enter_manually_popup)
    name_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    price_entry = tk.Entry(enter_manually_popup)
    price_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    date_entry = tk.Entry(enter_manually_popup)
    date_entry.grid(row=1, column=5, padx=10, pady=10, sticky="ew")

    # Create the drop-down list for category selection
    category_options = ["Food", "Personal", "Work", "Home", "Transportation", "Recurring", "Misc"]
    category_var = tk.StringVar(enter_manually_popup)
    category_combobox = ttk.Combobox(enter_manually_popup, textvariable=category_var, values=category_options,
                                     state="readonly")
    category_combobox.grid(row=1, column=3, padx=10, pady=10, sticky="ew")
    category_combobox.current(0)

    priority_options = ["High", "Medium", "Low"]
    priority_var = tk.StringVar(enter_manually_popup)
    priority_combobox = ttk.Combobox(enter_manually_popup, textvariable=priority_var, values=priority_options,
                                     state="readonly")
    priority_combobox.grid(row=1, column=4, padx=10, pady=10, sticky="ew")
    priority_combobox.current(0)

    # Create the Confirm button
    confirm_button = tk.Button(enter_manually_popup, text="Confirm",
                               command=lambda: add_expense(name_entry.get(), category_var.get(), price_entry.get(),
                                                           priority_var.get(), date_entry.get()))
    confirm_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")


def add_expense(name, category, price, priority, date):
    global funds_remaining

    price = float(price)
    funds_remaining -= price

    # Update the treeview with the new expense
    tree.insert("", "end", values=(name, category, "${:,.2f}".format(price), priority, date))

    # Update the remaining funds label
    funds_remaining_label.config(text="${:,.2f}".format(funds_remaining))

    # Update priority expense labels
    if priority == "High":
        current_text = high_priority_label.cget("text")
        current_amount = float(current_text.split(": $")[1])
        new_amount = current_amount + price
        high_priority_label.config(text="High priority expenses : ${:,.2f}".format(new_amount))
    elif priority == "Medium":
        current_text = medium_priority_label.cget("text")
        current_amount = float(current_text.split(": $")[1])
        new_amount = current_amount + price
        medium_priority_label.config(text="Medium priority expenses : ${:,.2f}".format(new_amount))
    else:
        current_text = low_priority_label.cget("text")
        current_amount = float(current_text.split(": $")[1])
        new_amount = current_amount + price
        low_priority_label.config(text="Low priority expenses : ${:,.2f}".format(new_amount))


# Call to method budget_window() that will start the program
budget_window()
