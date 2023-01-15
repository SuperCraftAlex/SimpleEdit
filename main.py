import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class TextEditor:
    def __init__(self, master):
        self.master = master
        master.title("Text Editor")

        # Create a notebook widget to hold multiple text widgets
        self.notebook = tk.ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both')

        # Create an empty dictionary to store the text widgets
        self.text_widgets = {}

        # Create a new text widget when the program starts
        self.new_file()

        self.menubar = tk.Menu(master)
        master.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open Folder", command=self.open_folder)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)
        
        self.settings_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Change Theme", command=self.settings)
    
    def new_file(self):
        # Create a new text widget and add it to the notebook
        text = tk.Text(self.notebook)
        self.notebook.add(text, text="Untitled")
        self.notebook.select(text)
        self.text_widgets[text] = {"filepath": None, "modified": False}

    def open_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            # Open the file and add its contents to a new text widget
            with open(filepath, 'r') as file:
                text = tk.Text(self.notebook)
                text.insert('1.0', file.read())
                self.notebook.add(text, text=filepath.split("/")[-1])
                self.notebook.select(text)
                self.text_widgets[text] = {"filepath": filepath, "modified": False}

    def save_file(self):
        text = self.notebook.select()
        if self.text_widgets[text]["filepath"]:
            # Save the contents of the current text widget to its associated file
            with open(self.text_widgets[text]["filepath"], 'w') as file:
                file.write(text.get('1.0', 'end'))
                self.text_widgets[text]["modified"] = False
        else:
            self.save_as_file()

    def save_as_file(self):
        text = self.notebook.select()
        filepath = filedialog.asksaveasfilename()
        if filepath:
            # Save the contents of the current text widget to a new file
            with open(filepath, 'w') as file:
                file.write(text.get('1.0', 'end'))
                self.notebook.tab(text, text=filepath.split("/")[-1])
                self.text_widgets[text]["filepath"] = filepath
                self.text_widgets[text]["modified"] = False
                
    def settings(self):
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title("Settings")
        self.themes = ["default", "dark", "light"]
        theme_var = tk.StringVar()
        theme_var.set(self.themes[0])
        theme_dropdown = tk.OptionMenu(self.settings_window, theme_var, *self.themes, command=self.change_theme)
        theme_dropdown.pack()

    def change_theme(self, theme):
        import themes
        theme_colors = getattr(themes, theme + "_theme")
        self.master.config(bg=theme_colors["background"])
        for text in self.text_widgets.values():
            text.config(bg=theme_colors["background"], fg=theme_colors["foreground"])
    
    def open_folder(self):
        folder_path = filedialog.askdirectory()

        # Create a treeview to display the folder structure
        self.tree = ttk.Treeview(self.notebook)
        self.tree.pack(fill='both', expand=True)
        self.notebook.add(self.tree, text="Folder Explorer")
        self.notebook.select(self.tree)

        # Insert the root folder into the treeview
        root_node = self.tree.insert('', 'end', text=folder_path.split("/")[-1], open=True)

        # Insert the subfolders and files into the treeview
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                child_node = self.tree.insert(root_node, 'end', text=item, open=False)
                self.insert_children(child_node, item_path)
            else:
                self.tree.insert(root_node, 'end', text=item)

    def insert_children(self, node, path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                child_node = self.tree.insert(node, 'end', text=item, open=False)
                self.insert_children(child_node, item_path)
            else:
                self.tree.insert(node, 'end', text=item)
    
    def close_tab(self, event):
        text = self.notebook.select()
        if self.text_widgets[text]["modified"]:
            answer = messagebox.askyesnocancel("Save Changes", "Would you like to save your changes?")
            if answer == True:
                self.save_file()
                self.notebook.forget(text)
                del self.text_widgets[text]
            elif answer == False:
                self.notebook.forget(text)
                del self.text_widgets[text]
        else:
            self.notebook.forget(text)
            del self.text_widgets[text]

root = tk.Tk()
editor = TextEditor(root)
root.mainloop()


