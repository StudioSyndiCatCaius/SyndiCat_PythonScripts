import tkinter as tk
from tkinter import ttk, filedialog
import re

class LuaPropertyEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Lua Property Editor")

        # Create File Selection UI
        self.file_label = ttk.Label(self.master, text="Lua File:")
        self.file_label.pack(pady=5)

        self.file_entry = ttk.Entry(self.master)
        self.file_entry.pack(fill='x', padx=10, pady=5)

        self.file_button = ttk.Button(self.master, text="Browse", command=self.select_lua_file)
        self.file_button.pack(pady=5)

        self.load_button = ttk.Button(self.master, text="Load", command=self.load_lua_file)
        self.load_button.pack(pady=10)

        # Create Property Editor UI (hidden initially)
        self.property_frame = ttk.Frame(self.master)
        self.tree = ttk.Treeview(self.property_frame)
        self.tree['columns'] = ('value',)
        self.tree.heading('#0', text='Property')
        self.tree.heading('value', text='Value')
        self.tree.pack(fill='both', expand=True)

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        self.value_entry = ttk.Entry(self.property_frame)
        self.value_entry.pack(fill='x')

        self.save_button = ttk.Button(self.property_frame, text="Save", command=self.save_changes)
        self.save_button.pack(fill='x')

        self.property_frame.pack_forget()

    def select_lua_file(self):
        self.lua_file = filedialog.askopenfilename(filetypes=[("Lua Files", "*.lua")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, self.lua_file)

    def load_lua_file(self):
        self.lua_file = self.file_entry.get()
        with open(self.lua_file, 'r') as file:
            self.lua_data = file.read()

        self.properties = self.parse_lua_properties(self.lua_data)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for name, value in self.properties.items():
            self.tree.insert('', 'end', text=name, values=(str(value),))

        self.property_frame.pack(fill='both', expand=True)

    def parse_lua_properties(self, lua_data):
        properties = {}
        for line in lua_data.splitlines():
            match = re.match(r'^\s*(\w+)\s*=\s*(\d+\.\d+|[-+]?\d+|true|false|".*?")\s*,?\s*$', line)
            if match:
                name = match.group(1)
                value = eval(match.group(2))
                properties[name] = value
        return properties

    def on_select(self, event):
        selected_item = self.tree.selection()[0]
        property_name = self.tree.item(selected_item, 'text')
        property_value = self.properties[property_name]
        self.value_entry.delete(0, tk.END)
        self.value_entry.insert(0, str(property_value))

    def save_changes(self):
        selected_item = self.tree.selection()[0]
        property_name = self.tree.item(selected_item, 'text')
        new_value = self.value_entry.get()

        try:
            new_value_type = type(self.properties[property_name])
            self.properties[property_name] = new_value_type(new_value)
            self.tree.item(selected_item, values=(new_value,))
            self.update_lua_file()
        except ValueError:
            print(f"Invalid value for {property_name}. Please enter a valid {new_value_type.__name__}.")

    def update_lua_file(self):
        new_lua_data = ''
        for name, value in self.properties.items():
            new_lua_data += f"{name} = {repr(value)},\n"
        with open(self.lua_file, 'w') as file:
            file.write(new_lua_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = LuaPropertyEditor(root)
    root.mainloop()