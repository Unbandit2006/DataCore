import customtkinter as ct
import tkinter as tk
from tkinter import ttk


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

        self.weekly_data = {
            "Days": ["Monday", "Tuesday", "Wednsday", "Thursday", "Friday", "Saturday", "Sunday"],
            "Amount of sales": [1, 2, 3, 11, 15, 18, 19]
        }

        self.yearly_data = {
            "Months": ["October", "November","December", "January", "Feburary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "Amount of sales": [0, 0, 3, 41, 28, 53, 36, 85, 25, 85, 89, 36, 52, 100, 56]
        }

        self.employees = {
            "Daniel Zheleznov": ["CEO", 70000, "123-456-789", "zheleznov.daniel@datacoreve.com", "Manager"],
            "Nadeyah Sharhan": ["COO", 65000, "379-756-6879", "sharhan.nadeyah@datacoreve.com", "Manager"],
            "Denis Trifonov": ["CSO", 65000, "403-173-7858", "trifonov.denis@datacoreve.com", "Manager"],
            "Bernie Yang": ["CTO", 65000, "361-723-0900", "yang.bernie@datacoreve.com", "Manager"],
            "Annie Wang": ["CFO", 65000, "992-649-0492", "wang.annie@datacoreve.com", "Manager"],
            "Janice Liu": ["CAO", 65000, "463-354-8754", "liu.janice@datacoreve.com", "Manager"],
            "Bekim Seferoviq": ["CMO", 65000, "144-602-8555", "seferoviq.bekim@datacoreve.com", "Manager"],
        }

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
        inventory = ct.CTkButton(self.sidebar, 230, text="Inventory", font=self.jetbrains_mono_mini)
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

        employee_listbox = tk.Listbox(self.info, font=self.jetbrains_mono)
        for employee in self.employees:
            employee_listbox.insert(tk.END, employee)
        employee_listbox.pack(side="left", expand=1, fill="both")

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

        employee_frame.pack( expand=1, fill="both")

        self.info.grid(column=1, row=0, sticky="nswe", columnspan=3, rowspan=4)

    def _base_cmd(self):
        self.info.destroy()
        self.canvas.unbind_all("<Configure>")
        self.info = ct.CTkFrame(self.root)

        self.info.grid(column=1, row=0, sticky="nswe", columnspan=3, rowspan=4)

app = DataCoreApp()
app.run()