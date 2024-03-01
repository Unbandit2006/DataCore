import customtkinter as ct

window = ct.CTk()
window.title("DataCore")
window.geometry("1280x720+100+50")

window.grid_rowconfigure((0, 1, 2), weight=1)
sidebar_frame = ct.CTkFrame(window, width=250, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")

jetbrains_mono = ct.CTkFont(family="JetBrains Mono Medium", size=25)
jetbrains_mono_mini = ct.CTkFont(family="JetBrains Mono Medium", size=14)

# title
title = ct.CTkLabel(sidebar_frame, 250, text="DataCore", font=jetbrains_mono)
title.grid(column=0, row=0, pady=(10, 10))

sales = ct.CTkButton(sidebar_frame, 230, text="Sales", font=jetbrains_mono_mini)
sales.grid(column=0, row=1, pady=5)

employee = ct.CTkButton(sidebar_frame, 230, text="Employee", font=jetbrains_mono_mini)
employee.grid(column=0, row=2, pady=5)

inventory = ct.CTkButton(sidebar_frame, 230, text="Inventory", font=jetbrains_mono_mini)
inventory.grid(column=0, row=3, pady=5)

window.mainloop()