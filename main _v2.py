import tkinter as tk
from tkinter import ttk, messagebox


class ModernUnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultra Modern Unit Converter")
        self.root.geometry("900x620")
        self.root.minsize(900, 620)
        self.root.configure(bg="#0f172a")

        self.history = []

        self.categories = {
            "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"],
            "Weight": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Time": ["Second", "Minute", "Hour", "Day"],
            "Speed": ["m/s", "km/h", "mph"],
        }

        self.setup_styles()
        self.build_ui()
        self.update_units()
        self.root.bind("<Return>", self.handle_enter)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TLabel",
            background="#0f172a",
            foreground="white",
            font=("Segoe UI", 11)
        )

        style.configure(
            "Title.TLabel",
            background="#0f172a",
            foreground="#38bdf8",
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Sub.TLabel",
            background="#0f172a",
            foreground="#94a3b8",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Card.TFrame",
            background="#1e293b"
        )

        style.configure(
            "TCombobox",
            fieldbackground="#334155",
            background="#334155",
            foreground="white",
            padding=8,
            font=("Segoe UI", 11)
        )

    def build_ui(self):
        header = tk.Frame(self.root, bg="#0f172a")
        header.pack(fill="x", padx=20, pady=(20, 10))

        ttk.Label(header, text="Ultra Modern Unit Converter", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Convert units quickly with clean UI, history, swap, and copy features.",
            style="Sub.TLabel"
        ).pack(anchor="w", pady=(4, 0))

        content = tk.Frame(self.root, bg="#0f172a")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        self.left_card = tk.Frame(content, bg="#1e293b", bd=0, highlightthickness=0)
        self.left_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.right_card = tk.Frame(content, bg="#1e293b", bd=0, highlightthickness=0, width=260)
        self.right_card.pack(side="right", fill="y")
        self.right_card.pack_propagate(False)

        self.build_converter_panel()
        self.build_history_panel()

    def build_converter_panel(self):
        container = self.left_card

        tk.Label(
            container,
            text="Converter Panel",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        form = tk.Frame(container, bg="#1e293b")
        form.pack(fill="both", expand=True, padx=20, pady=10)

        # Category
        tk.Label(form, text="Category", bg="#1e293b", fg="#cbd5e1", font=("Segoe UI", 11)).grid(
            row=0, column=0, sticky="w", pady=(5, 8)
        )
        self.category_var = tk.StringVar(value="Length")
        self.category_combo = ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=list(self.categories.keys()),
            state="readonly",
            width=28
        )
        self.category_combo.grid(row=1, column=0, sticky="ew", padx=(0, 12), pady=(0, 15))
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self.update_units())

        # Value
        tk.Label(form, text="Enter Value", bg="#1e293b", fg="#cbd5e1", font=("Segoe UI", 11)).grid(
            row=0, column=1, sticky="w", pady=(5, 8)
        )
        self.value_entry = tk.Entry(
            form,
            font=("Segoe UI", 12),
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=30
        )
        self.value_entry.grid(row=1, column=1, sticky="ew", pady=(0, 15))
        self.value_entry.focus()

        # From unit
        tk.Label(form, text="From Unit", bg="#1e293b", fg="#cbd5e1", font=("Segoe UI", 11)).grid(
            row=2, column=0, sticky="w", pady=(5, 8)
        )
        self.from_var = tk.StringVar()
        self.from_combo = ttk.Combobox(form, textvariable=self.from_var, state="readonly", width=28)
        self.from_combo.grid(row=3, column=0, sticky="ew", padx=(0, 12), pady=(0, 15))

        # To unit
        tk.Label(form, text="To Unit", bg="#1e293b", fg="#cbd5e1", font=("Segoe UI", 11)).grid(
            row=2, column=1, sticky="w", pady=(5, 8)
        )
        self.to_var = tk.StringVar()
        self.to_combo = ttk.Combobox(form, textvariable=self.to_var, state="readonly", width=28)
        self.to_combo.grid(row=3, column=1, sticky="ew", pady=(0, 15))

        # Buttons row 1
        button_row_1 = tk.Frame(form, bg="#1e293b")
        button_row_1.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 10))

        self.make_button(button_row_1, "Convert", self.convert_units, "#38bdf8", "black").pack(
            side="left", padx=(0, 10)
        )
        self.make_button(button_row_1, "Swap Units", self.swap_units, "#22c55e", "black").pack(
            side="left", padx=(0, 10)
        )
        self.make_button(button_row_1, "Clear", self.clear_fields, "#f59e0b", "black").pack(side="left")

        # Buttons row 2
        button_row_2 = tk.Frame(form, bg="#1e293b")
        button_row_2.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        self.make_button(button_row_2, "Copy Result", self.copy_result, "#a78bfa", "black").pack(side="left")

        # Result card
        result_card = tk.Frame(form, bg="#0f172a", bd=0, relief="flat")
        result_card.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 10))

        tk.Label(
            result_card,
            text="Result",
            bg="#0f172a",
            fg="#94a3b8",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self.result_var = tk.StringVar(value="No conversion yet")
        self.result_label = tk.Label(
            result_card,
            textvariable=self.result_var,
            bg="#0f172a",
            fg="#22c55e",
            font=("Segoe UI", 20, "bold"),
            wraplength=560,
            justify="left"
        )
        self.result_label.pack(anchor="w", padx=15, pady=(0, 15))

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

    def build_history_panel(self):
        container = self.right_card

        tk.Label(
            container,
            text="History",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=15, pady=(20, 10))

        tk.Label(
            container,
            text="Recent conversions",
            bg="#1e293b",
            fg="#94a3b8",
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=15, pady=(0, 10))

        self.history_listbox = tk.Listbox(
            container,
            bg="#0f172a",
            fg="white",
            font=("Consolas", 10),
            relief="flat",
            highlightthickness=0,
            selectbackground="#38bdf8",
            selectforeground="black"
        )
        self.history_listbox.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.make_button(container, "Clear History", self.clear_history, "#ef4444", "white").pack(
            padx=15, pady=(0, 15), fill="x"
        )

    def make_button(self, parent, text, command, bg, fg):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        )

    def update_units(self):
        category = self.category_var.get()
        units = self.categories.get(category, [])

        self.from_combo["values"] = units
        self.to_combo["values"] = units

        if units:
            self.from_var.set(units[0])
            self.to_var.set(units[1] if len(units) > 1 else units[0])

        self.result_var.set("No conversion yet")

    def handle_enter(self, event):
        self.convert_units()

    def swap_units(self):
        from_unit = self.from_var.get()
        to_unit = self.to_var.get()

        if from_unit and to_unit:
            self.from_var.set(to_unit)
            self.to_var.set(from_unit)

    def clear_fields(self):
        self.value_entry.delete(0, tk.END)
        self.result_var.set("No conversion yet")
        self.value_entry.focus()

    def clear_history(self):
        self.history.clear()
        self.history_listbox.delete(0, tk.END)

    def copy_result(self):
        result_text = self.result_var.get()
        if result_text == "No conversion yet":
            messagebox.showwarning("Nothing to Copy", "Please perform a conversion first.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(result_text)
        self.root.update()
        messagebox.showinfo("Copied", "Result copied to clipboard.")

    def convert_units(self):
        raw_value = self.value_entry.get().strip()

        if not raw_value:
            messagebox.showerror("Input Error", "Please enter a value.")
            return

        try:
            value = float(raw_value)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric value.")
            return

        category = self.category_var.get()
        from_unit = self.from_var.get()
        to_unit = self.to_var.get()

        try:
            result = self.convert(category, value, from_unit, to_unit)
            formatted_result = f"{value} {from_unit} = {result:.6f} {to_unit}"
            self.result_var.set(formatted_result)
            self.add_to_history(formatted_result)
        except Exception as error:
            messagebox.showerror("Conversion Error", str(error))

    def add_to_history(self, text):
        self.history.append(text)
        self.history_listbox.insert(tk.END, text)

    def convert(self, category, value, from_unit, to_unit):
        if category == "Length":
            return self.convert_length(value, from_unit, to_unit)
        if category == "Weight":
            return self.convert_weight(value, from_unit, to_unit)
        if category == "Temperature":
            return self.convert_temperature(value, from_unit, to_unit)
        if category == "Time":
            return self.convert_time(value, from_unit, to_unit)
        if category == "Speed":
            return self.convert_speed(value, from_unit, to_unit)

        raise ValueError("Unsupported category selected.")

    def convert_length(self, value, from_unit, to_unit):
        to_meter = {
            "Meter": 1.0,
            "Kilometer": 1000.0,
            "Centimeter": 0.01,
            "Millimeter": 0.001,
            "Mile": 1609.344,
            "Yard": 0.9144,
            "Foot": 0.3048,
            "Inch": 0.0254,
        }
        meters = value * to_meter[from_unit]
        return meters / to_meter[to_unit]

    def convert_weight(self, value, from_unit, to_unit):
        to_kg = {
            "Kilogram": 1.0,
            "Gram": 0.001,
            "Milligram": 0.000001,
            "Pound": 0.45359237,
            "Ounce": 0.028349523125,
        }
        kg = value * to_kg[from_unit]
        return kg / to_kg[to_unit]

    def convert_temperature(self, value, from_unit, to_unit):
        if from_unit == "Celsius":
            celsius = value
        elif from_unit == "Fahrenheit":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        else:
            raise ValueError("Invalid temperature unit.")

        if to_unit == "Celsius":
            return celsius
        elif to_unit == "Fahrenheit":
            return (celsius * 9 / 5) + 32
        elif to_unit == "Kelvin":
            return celsius + 273.15
        else:
            raise ValueError("Invalid temperature unit.")

    def convert_time(self, value, from_unit, to_unit):
        to_second = {
            "Second": 1.0,
            "Minute": 60.0,
            "Hour": 3600.0,
            "Day": 86400.0,
        }
        seconds = value * to_second[from_unit]
        return seconds / to_second[to_unit]

    def convert_speed(self, value, from_unit, to_unit):
        to_mps = {
            "m/s": 1.0,
            "km/h": 0.2777777778,
            "mph": 0.44704,
        }
        mps = value * to_mps[from_unit]
        return mps / to_mps[to_unit]


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernUnitConverter(root)
    root.mainloop()