import customtkinter as ct
import tkinter as tk
from tkinter import ttk
import json


class DataCoreApp:
    def __init__(self):
        self.root = ct.CTk()
        self.root.title("DataCore App DEMO")
        self.root.geometry("1280x720+100+50")

        self.jetbrains_mono = ct.CTkFont(family="JetBrains Mono Medium", size=25)
        self.jetbrains_mono_mini_big = ct.CTkFont(family="JetBrains Mono Medium", size=16)
        self.jetbrains_mono_mini = ct.CTkFont(family="JetBrains Mono Medium", size=14)

        self.sidebar = ct.CTkFrame(self.root, width=250, corner_radius=0)
        self.info = ct.CTkFrame(self.root)

        self.weekly_data = self.get_weekly_data()

        self.yearly_data = self.get_yearly_data()

        self.employees = self.get_employee_data()

    def run(self):
        self.root.grid_rowconfigure((0, 1, 2), weight=1)
        self.root.grid_columnconfigure((1, 2, 3), weight=1)
        self.sidebar.grid(row=0, column=0, rowspan=3, sticky="nsew")

        title = ct.CTkLabel(self.sidebar, 250, text="DataCore", font=self.jetbrains_mono)
        title.grid(column=0, row=0, pady=(10, 10))

        sales = ct.CTkButton(self.sidebar, 230, text="Sales", font=self.jetbrains_mono_mini, command=self.sales_cmd)
        sales.grid(column=0, row=1, pady=5)

        # employee
        employee = ct.CTkButton(self.sidebar, 230, text="Employee", font=self.jetbrains_mono_mini, command=self.employee_cmd)
        employee.grid(column=0, row=2, pady=5)

        # inventory
        inventory = ct.CTkButton(self.sidebar, 230, text="Inventory", font=self.jetbrains_mono_mini, command=self.inventory_cmd)
        inventory.grid(column=0, row=3, pady=5)

        version = ct.CTkLabel(self.sidebar, 230, text="Beta v3 (WIP)", font=self.jetbrains_mono_mini, text_color="green", anchor="s")
        version.grid(column=0, row=100)

        self.info.grid(column=1, row=0, sticky="nswe", columnspan=3, rowspan=4)

        self.root.mainloop()

    def sales_cmd(self):
        self.info.destroy()
        self.info = ct.CTkFrame(self.root)

        tab_view = ct.CTkTabview(self.info)

        weekly = tab_view.add("Weekly")
        yearly = tab_view.add("Yearly")
        tab_view.add("All sales")

        # weekly
        self.canvas = ct.CTkCanvas(weekly)
        self.canvas.pack(expand=1, fill="both")
        self.canvas.bind("<Configure>", self.update_bars_for_weekly)

        # yearly
        self.yearly_canvas = ct.CTkCanvas(yearly)
        self.yearly_canvas.pack(expand=1, fill="both")
        self.yearly_canvas.bind("<Configure>", self.update_bars_for_yearly)

        tab_view.pack(expand=1, fill="both")
        self.info.grid(column=1, row=0, sticky="nswe", columnspan=3, rowspan=4)

    def update_bars_for_weekly(self, event): # IDK AI MADE IT
        self.canvas.delete("all")
        width = event.width
        height = event.height
        bar_width = 0.8 * (width / len(self.weekly_data["Days"]))
        y_scale = 0.8 * (height / max(self.weekly_data["Amount of sales"]))

        for i in range(len(self.weekly_data["Days"])):
            x0 = i * (width / len(self.weekly_data["Days"])) + 0.1 * (width / len(self.weekly_data["Days"]))
            y0 = height - (self.weekly_data["Amount of sales"][i] * y_scale)
            x1 = x0 + bar_width
            y1 = height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
            self.canvas.create_text((x0 + x1) / 2, y0 - 10, text=f"{self.weekly_data['Days'][i]}||{self.weekly_data['Amount of sales'][i]}",
                                    font=self.jetbrains_mono_mini_big)

    def update_bars_for_yearly(self, event):
        self.yearly_canvas.delete("all")
        def generate_yearly_graph(canvas, width, height):
            bar_width = 0.7 * (width / len(self.yearly_data["Months"]))
            y_scale = 0.8 * (height / max(self.yearly_data["Amount of sales"]))

            for i in range(len(self.yearly_data["Amount of sales"])):
                x0 = i * (width / len(self.yearly_data["Months"])) + 0.1 * (width / len(self.yearly_data["Months"]))
                y0 = height - (self.yearly_data["Amount of sales"][i] * y_scale)
                x1 = x0 + bar_width
                y1 = height
                canvas.create_rectangle(x0, y0, x1, y1, fill="blue")

                if self.yearly_data["Amount of sales"][i] > 0:
                    canvas.create_text((x0 + x1) / 2, y0, text=f"{self.yearly_data['Amount of sales'][i]}",
                                        font=self.jetbrains_mono_mini_big)
                    canvas.create_text((x0 + x1) / 2, height-20, text=f"{self.yearly_data['Months'][i]}",
                                        font=self.jetbrains_mono_mini_big)


        generate_yearly_graph(self.yearly_canvas, event.width, event.height)

    def employee_cmd(self):
        self.info.destroy()
        self.info = ct.CTkFrame(self.root)

        self.employee_listbox = tk.Listbox(self.info, font=self.jetbrains_mono)
        for employee in self.employees:
            self.employee_listbox.insert(tk.END, employee)
        self.employee_listbox.bind("<<ListboxSelect>>", self.update_entries)
        self.employee_listbox.pack(side="left", expand=1, fill="both")

        employee_frame = tk.Frame(self.info)

        employee_name_lb = tk.Label(employee_frame, text="Name: ", font=self.jetbrains_mono, anchor="e", padx=0)
        employee_name_lb.grid(row=0, column=0)

        self.employee_name = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_name_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_name)
        employee_name_et.grid(row=0, column=1, columnspan=2)        

        employee_title_lb = tk.Label(employee_frame, text="Title: ", font=self.jetbrains_mono, anchor="e")
        employee_title_lb.grid(row=1, column=0)

        self.employee_title = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_title_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_title)
        employee_title_et.grid(row=1, column=1, columnspan=2)       

        employee_pay_lb = tk.Label(employee_frame, text="Pay: ", font=self.jetbrains_mono, anchor="e")
        employee_pay_lb.grid(row=2, column=0)

        self.employee_pay = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_pay_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_pay)
        employee_pay_et.grid(row=2, column=1, columnspan=2) 

        employee_phone_lb = tk.Label(employee_frame, text="Phone: ", font=self.jetbrains_mono, anchor="w")
        employee_phone_lb.grid(row=3, column=0)

        self.employee_phone = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_phone_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_phone)
        employee_phone_et.grid(row=3, column=1, columnspan=2) 

        employee_email_lb = tk.Label(employee_frame, text="Email: ", font=self.jetbrains_mono, anchor="w")
        employee_email_lb.grid(row=4, column=0)

        self.employee_email = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_email_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_email)
        employee_email_et.grid(row=4, column=1, columnspan=2) 

        employee_role_lb = tk.Label(employee_frame, text="Role: ", font=self.jetbrains_mono, anchor="e", padx=0)
        employee_role_lb.grid(row=5, column=0)

        self.employee_role = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_role_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_role)
        employee_role_et.grid(row=5, column=1, columnspan=2) 

        self.save_button = ct.CTkButton(employee_frame, text="Save", command=self.save_entries)
        self.save_button.grid(row=6, column=0, sticky="w", columnspan=3)  

        employee_frame.pack( expand=1, fill="both")

        self.info.grid(column=1, row=0, sticky="nswe", columnspan=3, rowspan=4)

    def inventory_cmd(self):
        self.info.destroy()
        self.info = ct.CTkFrame(self.root)

        self.employee_listbox = tk.Listbox(self.info, font=self.jetbrains_mono)
        for employee in self.employees:
            self.employee_listbox.insert(tk.END, employee)
        self.employee_listbox.bind("<<ListboxSelect>>", self.update_entries)
        self.employee_listbox.pack(side="left", expand=1, fill="both")

        employee_frame = tk.Frame(self.info)

        employee_name_lb = tk.Label(employee_frame, text="Name: ", font=self.jetbrains_mono, anchor="e", padx=0)
        employee_name_lb.grid(row=0, column=0)

        self.employee_name = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_name_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_name)
        employee_name_et.grid(row=0, column=1, columnspan=2)        

        employee_title_lb = tk.Label(employee_frame, text="Title: ", font=self.jetbrains_mono, anchor="e")
        employee_title_lb.grid(row=1, column=0)

        self.employee_title = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_title_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_title)
        employee_title_et.grid(row=1, column=1, columnspan=2)       

        employee_pay_lb = tk.Label(employee_frame, text="Pay: ", font=self.jetbrains_mono, anchor="e")
        employee_pay_lb.grid(row=2, column=0)

        self.employee_pay = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_pay_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_pay)
        employee_pay_et.grid(row=2, column=1, columnspan=2) 

        employee_phone_lb = tk.Label(employee_frame, text="Phone: ", font=self.jetbrains_mono, anchor="w")
        employee_phone_lb.grid(row=3, column=0)

        self.employee_phone = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_phone_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_phone)
        employee_phone_et.grid(row=3, column=1, columnspan=2) 

        employee_email_lb = tk.Label(employee_frame, text="Email: ", font=self.jetbrains_mono, anchor="w")
        employee_email_lb.grid(row=4, column=0)

        self.employee_email = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_email_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_email)
        employee_email_et.grid(row=4, column=1, columnspan=2) 

        employee_role_lb = tk.Label(employee_frame, text="Role: ", font=self.jetbrains_mono, anchor="e", padx=0)
        employee_role_lb.grid(row=5, column=0)

        self.employee_role = tk.StringVar(employee_frame, value="WILL AUTO FILL")
        employee_role_et = tk.Entry(employee_frame, font=self.jetbrains_mono, textvariable=self.employee_role)
        employee_role_et.grid(row=5, column=1, columnspan=2) 

        self.save_button = ct.CTkButton(employee_frame, text="Save", command=self.save_entries)
        self.save_button.grid(row=6, column=0, sticky="w", columnspan=3)  

        employee_frame.pack( expand=1, fill="both")

        self.info.grid(column=1, row=0, sticky="nswe", columnspan=3, rowspan=4)

    def update_entries(self, event):        
        if self.employee_listbox.curselection() != ():
            name = self.employee_listbox.get(self.employee_listbox.curselection()[0])
            for employee in self.employees:
                if employee == name:
                    self.employee_name.set(employee)
                    self.employee_title.set(self.employees[employee][0])
                    self.employee_pay.set(self.employees[employee][1])
                    self.employee_phone.set(self.employees[employee][2])
                    self.employee_email.set(self.employees[employee][3])
                    self.employee_role.set(self.employees[employee][4])

    def save_entries(self):
        with open("data.json") as file:
            data = json.load(file)
            data["employees"][self.employee_name.get()] = [
                self.employee_title.get(), 
                self.employee_pay.get(), 
                self.employee_phone.get(), 
                self.employee_email.get(), 
                self.employee_role.get()
            ]
            file.close()

    def _base_cmd(self):
        self.info.destroy()
        self.canvas.unbind_all("<Configure>")
        self.info = ct.CTkFrame(self.root)

        self.info.grid(column=1, row=0, sticky="nswe", columnspan=3, rowspan=4)

    def get_weekly_data(self):
        with open("data.json") as file:
            data = json.load(file)
            weekly_data = data["weekly_data"]
            file.close()
        return weekly_data

    def get_yearly_data(self):
        with open("data.json") as file:
            data = json.load(file)
            yearly_data = data["yearly_data"]
            file.close()
        return yearly_data

    def get_employee_data(self):
        with open("data.json") as file:
            data = json.load(file)
            employee_data = data["employees"]
            file.close()
        return employee_data

app = DataCoreApp()
app.run()