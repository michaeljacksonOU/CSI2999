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
    canvas.create_window(budget_window.winfo_screenwidth() // 2, budget_window.winfo_screenheight() // 2 - 50, window=label1)

    budget_amount = tk.Entry(budget_window, font=("Arial", 20))
    canvas.create_window(budget_window.winfo_screenwidth() // 2, budget_window.winfo_screenheight() // 2, window=budget_amount)

    confirm_button = tk.Button(budget_window, text="Confirm", command=lambda: close_budget_window(budget_amount.get()), font=("Arial", 20))
    canvas.create_window(budget_window.winfo_screenwidth() // 2, budget_window.winfo_screenheight() // 2 + 50, window=confirm_button)

    budget_window.mainloop()

def close_budget_window(budget):
    global funds_remaining
    budget_window.destroy()
    funds_remaining = float(budget)
    main_window(budget)

def main_window(budget):
    global root, funds_remaining_label, tree, tree1, tree2, tree3, high_priority_label, medium_priority_label, low_priority_label

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
    canvas.create_window(horizontal_gap, vertical_gap, width=frame_width, height=frame_height, window=frame1, anchor="nw")
    canvas.create_window(horizontal_gap * 2 + frame_width, vertical_gap, width=frame_width, height=frame_height, window=frame2, anchor="nw")
    canvas.create_window(horizontal_gap, vertical_gap * 2 + frame_height, width=frame_width, height=frame_height, window=frame3, anchor="nw")
    canvas.create_window(horizontal_gap * 2 + frame_width, vertical_gap * 2 + frame_height, width=frame_width, height=frame_height, window=frame4, anchor="nw")

    budget_amount = float(budget)

    label1 = tk.Label(frame1, text="Budget:", anchor="w", font=("Arial", 28), fg="grey")
    label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    budget_amount_label = tk.Label(frame1, text="${:,.2f}".format(budget_amount), anchor="w", font=("Arial", 28), fg="grey")
    budget_amount_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    label2 = tk.Label(frame1, text="Funds Remaining:", anchor="w", font=("Arial", 28), fg="grey")
    label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    funds_remaining_label = tk.Label(frame1, text="${:,.2f}".format(budget_amount), anchor="w", font=("Arial", 28), fg="grey")
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

    misc_label = tk.Label(frame3, text="Miscellaneous : $0", anchor="w", font=("Arial", 20), fg="grey")
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
    notebook.pack(expand=1, fill='both')

    load_expenses()
    root.mainloop()

def load_expenses():
    global funds_remaining, funds_remaining_label, high_priority_label, medium_priority_label, low_priority_label
    if not os.path.isfile(expense_file):
        return

    df = pd.read_excel(expense_file)
    for _, row in df.iterrows():
        price = float(str(row["Price"]).replace('$', '').replace(',', ''))
        tree.insert("", "end", values=(row["Name"], row["Type"], f"${price:,.2f}", row["Priority"], row["Date"]))

        if row["Priority"] == "High":
            current_high = float(high_priority_label["text"].split("$")[1].replace(",", ""))
            current_high += price
            high_priority_label["text"] = f"High priority expenses: ${current_high:,.2f}"

            tree1.insert("", "end", values=(row["Name"], row["Type"], f"${price:,.2f}", row["Date"]))

        elif row["Priority"] == "Medium":
            current_medium = float(medium_priority_label["text"].split("$")[1].replace(",", ""))
            current_medium += price
            medium_priority_label["text"] = f"Medium priority expenses: ${current_medium:,.2f}"

            tree2.insert("", "end", values=(row["Name"], row["Type"], f"${price:,.2f}", row["Date"]))

        elif row["Priority"] == "Low":
            current_low = float(low_priority_label["text"].split("$")[1].replace(",", ""))
            current_low += price
            low_priority_label["text"] = f"Low priority expenses: ${current_low:,.2f}"

            tree3.insert("", "end", values=(row["Name"], row["Type"], f"${price:,.2f}", row["Date"]))

        funds_remaining -= price
        funds_remaining_label["text"] = "${:,.2f}".format(funds_remaining)

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
    global enter_manually_popup_window, expense_name_entry, expense_type_entry, expense_price_entry, priority_var, cal
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


    date_entry = DateEntry(enter_manually_popup_window, width=18, background='darkblue', foreground='white', borderwidth=2)
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

def add_expense(expense_name, expense_type, expense_price, priority, date):
    global funds_remaining,tree, tree1, tree2, tree3
   

    if expense_name and expense_type and expense_price and priority:
        expense_price = float(expense_price)
        tree.insert("", "end", values=(expense_name, expense_type,"${:,.2f}".format(expense_price), priority, date))

        if priority == "High":
            tree1.insert("", "end", values=(expense_name, expense_type, "${:,.2f}".format(expense_price), date))
        elif priority == "Medium":
            tree2.insert("", "end", values=(expense_name, expense_type, "${:,.2f}".format(expense_price), date))
        elif priority == "Low":
            tree3.insert("", "end", values=(expense_name, expense_type, "${:,.2f}".format(expense_price), date))

        funds_remaining -= expense_price
        funds_remaining_label.config(text="${:,.2f}".format(funds_remaining))
        update_labels()
        save_to_excel()
    else:
        messagebox.showerror("Input Error", "Please fill all fields")

def delete_expense():
    global funds_remaining
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Selection error", "Please select an expense to delete")
        return
    for item in selected_item:

        priority = tree.item(item)["values"][3]
        
        price = float(tree.item(item)["values"][2].replace("$", "").replace(",", ""))
        funds_remaining += price
        tree.delete(item)

    if priority == "High":
            for child in tree1.get_children():
                if tree1.item(child)["values"][0] == item:
                    tree1.delete(child)
                    break
    elif priority == "Medium":
            for child in tree2.get_children():
                if tree2.item(child)["values"][0] == item:
                    tree2.delete(child)
                    break
    elif priority == "Low":
            for child in tree3.get_children():
                if tree3.item(child)["values"][0] == item:
                    tree3.delete(child)
                    break
    update_labels()
    save_to_excel()

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

budget_window()