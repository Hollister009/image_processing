import tkinter as tk
from tkinter import ttk

class CustomDialog:
    """Custom dialog class."""

    def __init__(self, parent, title, fields, options):
        self.parent = parent
        self.title = title
        self.fields = fields
        self.options = options
        self.result = None

    def show(self):
        # Create the dialog window
        self.top = tk.Toplevel(self.parent)
        self.top.title(self.title)

        # Create a dict to hold the field values
        self.result = {}

        # Add the fields to the dialog
        for field in self.fields:
            # Create a label for the field
            label = ttk.Label(self.top, text=field[0])
            label.pack(side="top", padx=5, pady=5)

            if len(field) == 2:
                # If the field has only a default value, create an entry widget
                entry = ttk.Entry(self.top)
                entry.insert(0, str(field[1]))
                entry.pack(side="top", padx=5, pady=5)

            elif len(field) == 3 and field[2] == "select":
                # If the field has options, create a combobox widget
                options = self.options[field[0]]
                entry = ttk.Combobox(self.top, values=options)
                entry.pack(side="top", padx=5, pady=5)

            else:
                # Otherwise, create a standard entry widget
                entry = ttk.Entry(self.top)
                entry.pack(side="top", padx=5, pady=5)

            self.result[field[0]] = entry

        # Add an OK button to the dialog
        ok_button = ttk.Button(self.top, text="OK", command=self.ok)
        ok_button.pack(side="left", padx=5, pady=5)

        # Add a Cancel button to the dialog
        cancel_button = ttk.Button(self.top, text="Cancel", command=self.cancel)
        cancel_button.pack(side="right", padx=5, pady=5)

        # Wait for user input
        self.top.wait_window()

        return self.result

    def ok(self):
        # Save the entered values to self.result
        for field in self.fields:
            self.result[field[0]] = self.result[field[0]].get()

        self.top.destroy()

    def cancel(self):
        # Set the result to None and return
        self.result = None
        self.top.destroy()
