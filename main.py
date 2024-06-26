import clarity
import charity

settings = clarity.Settings.from_json_file("Config\\settings.json")
root = clarity.Window("DataCore Demo App", 1280, 720, settings)

tab_menu = clarity.TabMenu(settings)
# NOTE: The inital args for the tabs doesn't matter as the TabMenu will take care of that
tab_menu.add_tab("Employee Management", charity.EmployeeManagement(settings))
tab_menu.add_tab("Inventory Management", charity.InventoryManagement(settings))  
tab_menu.add_tab("Sales Management", charity.SalesManagement(settings))
root.add(tab_menu)

root.run()
