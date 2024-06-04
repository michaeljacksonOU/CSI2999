import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import os


funds_remaining = 0
expense_file = "expenses.xlsx"

def set_theme(window):

    window.tk.call("source", "Azure/azure.tcl")

    window.tk.call("set_theme", "dark")

#PIl
def set_background(window):
    image = Image.open("GRADIENT-BLUE.png")
    photo = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(window, width=1920, height=1080)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=photo, anchor="nw")
    window.photo = photo  # reference to photo
    return canvas


def budget_window():
    global funds_remaining, budget_window

    budget_window = tk.Tk()
    budget_window.title("Monthly Budget")
    budget_window.geometry("1920x1080")


    set_theme(budget_window)
    canvas = set_background(budget_window)

    label1 = tk.Label(budget_window, text="Enter your monthly budget:", font=("Arial", 23), bg="skyblue", fg="black")
    canvas.create_window(960, 350, window=label1)

    budget_amount = tk.Entry(budget_window, font=("Arial", 20))
    canvas.create_window(960, 400, window=budget_amount)

    confirm_button = tk.Button(budget_window, text="Confirm", command=lambda: close_budget_window(budget_amount.get()), font=("Arial", 20))
    canvas.create_window(960, 450, window=confirm_button)

    budget_window.mainloop()


def close_budget_window(budget):
    global funds_remaining
    budget_window.destroy()

    funds_remaining = float(budget)

    main_window(budget)


# tkinter and PIL
def main_window(budget):
    global root, funds_remaining_label, tree, high_priority_label, medium_priority_label, low_priority_label

    root = tk.Tk()
    root.title("Budget Tracker")
    root.geometry("1920x1080")

    set_theme(root)
    canvas = set_background(root)

    frame1 = tk.Frame(root, width=750, height=350)
    frame2 = tk.Frame(root, width=760, height=350)
    frame3 = tk.Frame(root, width=750, height=350)
    frame4 = tk.Frame(root, width=750, height=350)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    frame1.grid_propagate(False)
    frame2.grid_propagate(False)
    frame3.grid_propagate(False)
    frame4.grid_propagate(False)


    canvas.create_window(180, 125, window=frame1, anchor="nw")
    canvas.create_window(990, 125, window=frame2, anchor="nw")
    canvas.create_window(180, 500, window=frame3, anchor="nw")
    canvas.create_window(990, 500, window=frame4, anchor="nw")

    budget_amount = float(budget)

    label1 = tk.Label(frame1, text="Budget:", anchor="w", font=("Arial", 28), fg="grey")
    label1.grid(row=0, column=0, padx=25, pady=25, sticky="w")

    budget_amount_label = tk.Label(frame1, text="${:,.2f}".format(budget_amount), anchor="w", font=("Arial", 28), fg="grey")
    budget_amount_label.grid(row=0, column=1, padx=25, pady=25, sticky="w")

    label2 = tk.Label(frame1, text="Funds Remaining:", anchor="w", font=("Arial", 28), fg="grey")
    label2.grid(row=1, column=0, padx=25, pady=25, sticky="w")

    funds_remaining_label = tk.Label(frame1, text="${:,.2f}".format(budget_amount), anchor="w", font=("Arial", 28), fg="grey")
    funds_remaining_label.grid(row=1, column=1, padx=25, pady=25, sticky="w")


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
    canvas.create_window(960, 900, window=add_new_expense_button)

    delete_expense_button = tk.Button(root, text="Delete Expense", command=delete_expense)
    canvas.create_window(960, 950, window=delete_expense_button)

    high_priority_label = tk.Label(frame3, text="High priority expenses: $0", anchor="w", font=("Arial", 28), fg="grey")
    high_priority_label.grid(row=0, column=0, padx=25, pady=25, sticky="w")

    medium_priority_label = tk.Label(frame3, text="Medium priority expenses: $0", anchor="w", font=("Arial", 28), fg="grey")
    medium_priority_label.grid(row=1, column=0, padx=25, pady=25, sticky="w")

    low_priority_label = tk.Label(frame3, text="Low priority expenses: $0", anchor="w", font=("Arial", 28), fg="grey")
    low_priority_label.grid(row=2, column=0, padx=25, pady=25, sticky="w")

    style = ttk.Style()
    style.configure("TNotebook.Tab", font=('Helvetica', 25, 'bold'), padding=[40, 0])
    notebook = ttk.Notebook(frame4, style="TNotebook")

    tab1 = ttk.Frame(notebook)
    tree1 = ttk.Treeview(tab1, columns=("Name", "Type", "Price", "Date"), show="headings")
    tree1.column(col, width=90, anchor="w", stretch=tk.YES)
    tree1.heading("Name", text="Name")
    tree1.heading("Type", text="Type")
    tree1.heading("Price", text="Price")
    tree1.heading("Date", text="Date")
    scrollbar1 = ttk.Scrollbar(tab1, orient="vertical", command=tree.yview)
    tree1.configure(yscrollcommand=scrollbar1.set)
    tree1.pack(side="left", fill="both", expand=True)
    scrollbar1.pack(side="right", fill="y")

    tab2 = ttk.Frame(notebook)
    tree2 = ttk.Treeview(tab2, columns=("Name", "Type", "Price", "Date"), show="headings")
    tree2.column(col, width=90, anchor="w", stretch=tk.YES)
    tree2.heading("Name", text="Name")
    tree2.heading("Type", text="Type")
    tree2.heading("Price", text="Price")
    tree2.heading("Date", text="Date")
    scrollbar2 = ttk.Scrollbar(tab2, orient="vertical", command=tree.yview)
    tree2.configure(yscrollcommand=scrollbar2.set)
    tree2.pack(side="left", fill="both", expand=True)
    scrollbar2.pack(side="right", fill="y")
    tree2.pack()

    tab3 = ttk.Frame(notebook)
    tree3 = ttk.Treeview(tab3, columns=("Name", "Type", "Price", "Date"), show="headings")
    tree3.column(col, width=90, anchor="w", stretch=tk.YES)
    tree3.heading("Name", text="Name")
    tree3.heading("Type", text="Type")
    tree3.heading("Price", text="Price")
    tree3.heading("Date", text="Date")
    scrollbar3 = ttk.Scrollbar(tab3, orient="vertical", command=tree.yview)
    tree3.configure(yscrollcommand=scrollbar3.set)
    tree3.pack(side="left", fill="both", expand=True)
    scrollbar3.pack(side="right", fill="y")

    notebook.add(tab1, text="High")
    notebook.add(tab2, text="Medium")
    notebook.add(tab3, text="Low")
    notebook.pack(expand=1, fill='both')


    load_expenses()

    root.mainloop()


def load_expenses():
    global funds_remaining

    if os.path.exists(expense_file):
        df = pd.read_excel(expense_file)
        for index, row in df.iterrows():
            tree.insert("", "end", values=(row["Name"], row["Type"], row["Price"], row["Priority"], row["Date"]))
            funds_remaining -= row["Price"]

        update_labels()


def update_labels():
    total_high = total_medium = total_low = 0
    for child in tree.get_children():
        priority = tree.item(child)["values"][3]
        price = float(tree.item(child)["values"][2].replace("$", "").replace(",", ""))

        if priority == "High":
            total_high += price
        elif priority == "Medium":
            total_medium += price
        else:
            total_low += price

    high_priority_label.config(text="High priority expenses: ${:,.2f}".format(total_high))
    medium_priority_label.config(text="Medium priority expenses: ${:,.2f}".format(total_medium))
    low_priority_label.config(text="Low priority expenses: ${:,.2f}".format(total_low))
    funds_remaining_label.config(text="${:,.2f}".format(funds_remaining))

# storage into excel
def save_to_excel():
    expenses = []
    for child in tree.get_children():
        expenses.append(tree.item(child)["values"])

    df = pd.DataFrame(expenses, columns=["Name", "Type", "Price", "Priority", "Date"])
    df.to_excel(expense_file, index=False)


def expense_popup():
    global expense_window

    expense_window = tk.Toplevel()
    expense_window.title("Add New Expense")
    expense_window.geometry("400x300")

    canvas = set_background(expense_window)

    manual_button = tk.Button(expense_window, text="Enter Manually", command=close_expense_popup)
    canvas.create_window(200, 100, window=manual_button)

    upload_button = tk.Button(expense_window, text="Upload Receipt")
    canvas.create_window(200, 200, window=upload_button)


def close_expense_popup():
    expense_window.destroy()
    enter_manually_popup()


def enter_manually_popup():
    global enter_manually_popup_window

    enter_manually_popup_window = tk.Toplevel()
    enter_manually_popup_window.title("Manual Expense Entry")
    enter_manually_popup_window.geometry("800x150")

    name_label = tk.Label(enter_manually_popup_window, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    price_label = tk.Label(enter_manually_popup_window, text="Price:")
    price_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    category_label = tk.Label(enter_manually_popup_window, text="Category:")
    category_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    priority_label = tk.Label(enter_manually_popup_window, text="Priority:")
    priority_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")

    date_label = tk.Label(enter_manually_popup_window, text="Date:")
    date_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")

    name_entry = tk.Entry(enter_manually_popup_window)
    name_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    price_entry = tk.Entry(enter_manually_popup_window)
    price_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    date_entry = tk.Entry(enter_manually_popup_window)
    date_entry.grid(row=1, column=4, padx=10, pady=10, sticky="ew")

    category_options = ["Food", "Personal", "Work", "Home", "Transportation", "Recurring", "Misc"]
    category_var = tk.StringVar(enter_manually_popup_window)
    category_combobox = ttk.Combobox(enter_manually_popup_window, textvariable=category_var, values=category_options, state="readonly")
    category_combobox.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
    category_combobox.current(0)

    priority_options = ["High", "Medium", "Low"]
    priority_var = tk.StringVar(enter_manually_popup_window)
    priority_combobox = ttk.Combobox(enter_manually_popup_window, textvariable=priority_var, values=priority_options, state="readonly")
    priority_combobox.grid(row=1, column=3, padx=10, pady=10, sticky="ew")
    priority_combobox.current(0)

    confirm_button = tk.Button(enter_manually_popup_window, text="Confirm", command=lambda: add_expense(name_entry.get(), category_var.get(), price_entry.get(), priority_var.get(), date_entry.get()))
    confirm_button.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")


def add_expense(name, category, price, priority, date):
    global funds_remaining

    price = float(price)
    funds_remaining -= price

    tree.insert("", "end", values=(name, category, "${:,.2f}".format(price), priority, date))
    update_labels()
    save_to_excel()

    enter_manually_popup_window.destroy()


def delete_expense():
    global funds_remaining

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Selection error", "Please select an expense to delete")
        return

    for item in selected_item:
        price = float(tree.item(item)["values"][2].replace("$", "").replace(",", ""))
        funds_remaining += price
        tree.delete(item)

    update_labels()
    save_to_excel()


budget_window()
