import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import os
from tkcalendar import DateEntry

funds_remaining = 0
expense_file = "expenses.xlsx"


def set_theme(window):
    try:
        window.tk.call("source", "Azure/azure.tcl")
        window.tk.call("set_theme", "dark")
    except tk.TclError:
        pass  # Theme already set


def set_background(window):
    image = Image.open("GRADIENT-BLUE.png")
    photo = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=photo, anchor="nw")
    window.photo = photo  # Reference to photo
    return canvas


def budget_window():
    global funds_remaining, budget_window

    budget_window = tk.Tk()
    budget_window.title("Monthly Budget")
    budget_window.geometry(f"{budget_window.winfo_screenwidth()}x{budget_window.winfo_screenheight()}")

    set_theme(budget_window)
    canvas = set_background(budget_window)

    label1 = tk.Label(budget_window, text="Enter your monthly budget:", font=("Arial", 23), bg="skyblue", fg="black")
    canvas.create_window(budget_window.winfo_screenwidth() // 2, budget_window.winfo_screenheight() // 2 - 50,
                         window=label1)

    budget_amount = tk.Entry(budget_window, font=("Arial", 20))
    canvas.create_window(budget_window.winfo_screenwidth() // 2, budget_window.winfo_screenheight() // 2,
                         window=budget_amount)

    confirm_button = tk.Button(budget_window, text="Confirm", command=lambda: close_budget_window(budget_amount.get()),
                               font=("Arial", 20))
    canvas.create_window(budget_window.winfo_screenwidth() // 2, budget_window.winfo_screenheight() // 2 + 50,
                         window=confirm_button)

    budget_window.mainloop()


def close_budget_window(budget):
    global funds_remaining
    budget_window.destroy()
    funds_remaining = float(budget)
    main_window(budget)


def main_window(budget):
    global root, funds_remaining_label, tree, tree1, tree2, tree3, food_label, personal_label, work_label, home_label, transportation_label, recurring_label, misc_label

    root = tk.Tk()
    root.title("Budget Tracker")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    set_theme(root)
    canvas = set_background(root)

    frame1 = tk.Frame(root)
    frame2 = tk.Frame(root)
    frame3 = tk.Frame(root)
    frame4 = tk.Frame(root)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    canvas_width = root.winfo_screenwidth()
    canvas_height = root.winfo_screenheight()

    frame_width = canvas_width * 0.45
    frame_height = canvas_height * 0.35

    # Calculate the horizontal and vertical gap between frames
    horizontal_gap = canvas_width * 0.03
    vertical_gap = canvas_width * 0.04

    # Create windows for each frame
    canvas.create_window(horizontal_gap, vertical_gap, width=frame_width, height=frame_height, window=frame1,
                         anchor="nw")
    canvas.create_window(horizontal_gap * 2 + frame_width, vertical_gap, width=frame_width, height=frame_height,
                         window=frame2, anchor="nw")
    canvas.create_window(horizontal_gap, vertical_gap * 2 + frame_height, width=frame_width, height=frame_height,
                         window=frame3, anchor="nw")
    canvas.create_window(horizontal_gap * 2 + frame_width, vertical_gap * 2 + frame_height, width=frame_width,
                         height=frame_height, window=frame4, anchor="nw")

    budget_amount = float(budget)

    label1 = tk.Label(frame1, text="Budget:", anchor="w", font=("Arial", 28), fg="grey")
    label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    budget_amount_label = tk.Label(frame1, text="${:,.2f}".format(budget_amount), anchor="w", font=("Arial", 28),
                                   fg="grey")
    budget_amount_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    label2 = tk.Label(frame1, text="Funds Remaining:", anchor="w", font=("Arial", 28), fg="grey")
    label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    funds_remaining_label = tk.Label(frame1, text="${:,.2f}".format(budget_amount), anchor="w", font=("Arial", 28),
                                     fg="grey")
    funds_remaining_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    tree = ttk.Treeview(frame2, show="headings")
    tree["columns"] = ("Name", "Type", "Price", "Priority", "Date")

    for col in tree["columns"]:
        tree.column(col, width=150, anchor="w", stretch="YES")
        tree.heading(col, text=col, anchor="w")

    scrollbar = ttk.Scrollbar(frame2, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')

    tree.configure(yscrollcommand=scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")

    frame2.grid_rowconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)

    add_new_expense_button = tk.Button(root, text="Add New Expense", command=expense_popup)
    canvas.create_window(root.winfo_screenwidth() // 2, root.winfo_screenheight() - 100, window=add_new_expense_button)

    delete_expense_button = tk.Button(root, text="Delete Expense", command=delete_expense)
    canvas.create_window(890, 764, window=delete_expense_button)

    food_label = tk.Label(frame3, text="Food: $0", anchor="w", font=("Arial", 20), fg="grey")
    food_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    personal_label = tk.Label(frame3, text="Personal: $0", anchor="w", font=("Arial", 20), fg="grey")
    personal_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    work_label = tk.Label(frame3, text="Work: $0", anchor="w", font=("Arial", 20), fg="grey")
    work_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    home_label = tk.Label(frame3, text="Home: $0", anchor="w", font=("Arial", 20), fg="grey")
    home_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    transportation_label = tk.Label(frame3, text="Transportation: $0", anchor="w", font=("Arial", 20), fg="grey")
    transportation_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    recurring_label = tk.Label(frame3, text="Recurring: $0", anchor="w", font=("Arial", 20), fg="grey")
    recurring_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    misc_label = tk.Label(frame3, text="Miscellaneous: $0", anchor="w", font=("Arial", 20), fg="grey")
    misc_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

    style = ttk.Style()
    style.configure("TNotebook.Tab", font=('Helvetica', 25, 'bold'), padding=[40, 0])
    notebook = ttk.Notebook(frame4, style="TNotebook")

    tab1 = ttk.Frame(notebook)
    tree1 = ttk.Treeview(tab1, columns=("Name", "Type", "Price", "Date"), show="headings")
    for col in ("Name", "Type", "Price", "Date"):
        tree1.column(col, width=90, anchor="w", stretch=tk.YES)
        tree1.heading(col, text=col)
    scrollbar1 = ttk.Scrollbar(tab1, orient="vertical", command=tree1.yview)
    tree1.configure(yscrollcommand=scrollbar1.set)
    tree1.pack(side="left", fill="both", expand=True)
    scrollbar1.pack(side="right", fill="y")

    tab2 = ttk.Frame(notebook)
    tree2 = ttk.Treeview(tab2, columns=("Name", "Type", "Price", "Date"), show="headings")
    for col in ("Name", "Type", "Price", "Date"):
        tree2.column(col, width=90, anchor="w", stretch=tk.YES)
        tree2.heading(col, text=col)
    scrollbar2 = ttk.Scrollbar(tab2, orient="vertical", command=tree2.yview)
    tree2.configure(yscrollcommand=scrollbar2.set)
    tree2.pack(side="left", fill="both", expand=True)
    scrollbar2.pack(side="right", fill="y")

    tab3 = ttk.Frame(notebook)
    tree3 = ttk.Treeview(tab3, columns=("Name", "Type", "Price", "Date"), show="headings")
    for col in ("Name", "Type", "Price", "Date"):
        tree3.column(col, width=90, anchor="w", stretch=tk.YES)
        tree3.heading(col, text=col)
    scrollbar3 = ttk.Scrollbar(tab3, orient="vertical", command=tree3.yview)
    tree3.configure(yscrollcommand=scrollbar3.set)
    tree3.pack(side="left", fill="both", expand=True)
    scrollbar3.pack(side="right", fill="y")

    notebook.add(tab1, text="High")
    notebook.add(tab2, text="Medium")
    notebook.add(tab3, text="Low")
    notebook.pack(fill="both", expand=True)
    frame4.grid_columnconfigure(0, weight=1)
    frame4.grid_rowconfigure(0, weight=1)

    root.mainloop()


def expense_popup():
    global popup, entry1, entry2, entry3, priority_combobox, date_entry

    popup = tk.Toplevel(root)
    popup.title("Add New Expense")
    popup.geometry("300x300")

    label1 = tk.Label(popup, text="Expense Name:")
    label1.pack()
    entry1 = tk.Entry(popup)
    entry1.pack()

    label2 = tk.Label(popup, text="Expense Type:")
    label2.pack()
    expense_types = ["Food", "Personal", "Work", "Home", "Transportation", "Recurring", "Miscellaneous"]
    entry2 = ttk.Combobox(popup, values=expense_types)
    entry2.pack()

    label3 = tk.Label(popup, text="Expense Price:")
    label3.pack()
    entry3 = tk.Entry(popup)
    entry3.pack()

    label4 = tk.Label(popup, text="Expense Priority:")
    label4.pack()
    priority_combobox = ttk.Combobox(popup, values=["High", "Medium", "Low"])
    priority_combobox.pack()

    label5 = tk.Label(popup, text="Expense Date:")
    label5.pack()
    date_entry = DateEntry(popup, date_pattern="yyyy-mm-dd")
    date_entry.pack()

    add_button = tk.Button(popup, text="Add", command=add_expense)
    add_button.pack()


def add_expense():
    global funds_remaining

    name = entry1.get()
    expense_type = entry2.get()
    price = float(entry3.get())
    priority = priority_combobox.get()
    date = date_entry.get_date()

    funds_remaining -= price
    funds_remaining_label.config(text="${:,.2f}".format(funds_remaining))

    tree.insert("", "end", values=(name, expense_type, price, priority, date))

    if priority == "High":
        tree1.insert("", "end", values=(name, expense_type, price, date))
    elif priority == "Medium":
        tree2.insert("", "end", values=(name, expense_type, price, date))
    else:
        tree3.insert("", "end", values=(name, expense_type, price, date))

    update_labels(expense_type, price)
    save_to_excel(name, expense_type, price, priority, date)
    popup.destroy()


def update_labels(expense_type, price):
    labels = {
        "Food": food_label,
        "Personal": personal_label,
        "Work": work_label,
        "Home": home_label,
        "Transportation": transportation_label,
        "Recurring": recurring_label,
        "Miscellaneous": misc_label
    }

    current_text = labels[expense_type].cget("text")
    current_amount = float(current_text.split("$")[1].replace(",", ""))
    new_amount = current_amount + price
    labels[expense_type].config(text=f"{expense_type}: ${new_amount:,.2f}")


def save_to_excel(name, expense_type, price, priority, date):
    if os.path.exists(expense_file):
        df = pd.read_excel(expense_file)
    else:
        df = pd.DataFrame(columns=["Name", "Type", "Price", "Priority", "Date"])

    new_row = {"Name": name, "Type": expense_type, "Price": price, "Priority": priority, "Date": date}
    df = df.append(new_row, ignore_index=True)
    df.to_excel(expense_file, index=False)


def delete_expense():
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, "values")
    tree.delete(selected_item)

    if values[3] == "High":
        for item in tree1.get_children():
            if tree1.item(item, "values")[0] == values[0]:
                tree1.delete(item)
                break
    elif values[3] == "Medium":
        for item in tree2.get_children():
            if tree2.item(item, "values")[0] == values[0]:
                tree2.delete(item)
                break
    elif values[3] == "Low":
        for item in tree3.get_children():
            if tree3.item(item, "values")[0] == values[0]:
                tree3.delete(item)
                break

    price = float(values[2])
    funds_remaining += price
    funds_remaining_label.config(text="${:,.2f}".format(funds_remaining))

    update_labels_after_deletion(values[1], price)
    remove_from_excel(values[0])


def update_labels_after_deletion(expense_type, price):
    labels = {
        "Food": food_label,
        "Personal": personal_label,
        "Work": work_label,
        "Home": home_label,
        "Transportation": transportation_label,
        "Recurring": recurring_label,
        "Miscellaneous": misc_label
    }

    current_text = labels[expense_type].cget("text")
    current_amount = float(current_text.split("$")[1].replace(",", ""))
    new_amount = current_amount - price
    labels[expense_type].config(text=f"{expense_type}: ${new_amount:,.2f}")


def remove_from_excel(expense_name):
    if os.path.exists(expense_file):
        df = pd.read_excel(expense_file)
        df = df[df["Name"] != expense_name]
        df.to_excel(expense_file, index=False)


budget_window()
