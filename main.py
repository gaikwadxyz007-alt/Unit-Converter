import tkinter as tk
from tkinter import ttk, messagebox


class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Unit Converter")
        self.root.geometry("620x500")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.categories = {
            "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"],
            "Weight": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Time": ["Second", "Minute", "Hour", "Day"],
            "Speed": ["m/s", "km/h", "mph"],
        }

        self.create_styles()
        self.create_widgets()
        self.update_units()

    def create_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TLabel",
            background="#1e1e1e",
            foreground="white",
            font=("Segoe UI", 12)
        )

        style.configure(
            "Title.TLabel",
            background="#1e1e1e",
            foreground="#00d4ff",
            font=("Segoe UI", 22, "bold")
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10
        )

        style.configure(
            "TCombobox",
            font=("Segoe UI", 11),
            padding=6
        )

        style.configure(
            "TEntry",
            font=("Segoe UI", 11),
            padding=6
        )

    def create_widgets(self):
        title = ttk.Label(self.root, text="Smart Unit Converter", style="Title.TLabel")
        title.pack(pady=20)

        main_frame = tk.Frame(self.root, bg="#2b2b2b", bd=0, relief="flat")
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Category
        ttk.Label(main_frame, text="Select Category:").grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.category_var = tk.StringVar(value="Length")
        self.category_combo = ttk.Combobox(
            main_frame,
            textvariable=self.category_var,
            values=list(self.categories.keys()),
            state="readonly",
            width=25
        )
        self.category_combo.grid(row=0, column=1, padx=15, pady=15)
        self.category_combo.bind("<<ComboboxSelected>>", lambda event: self.update_units())

        # Input value
        ttk.Label(main_frame, text="Enter Value:").grid(row=1, column=0, padx=15, pady=15, sticky="w")
        self.value_entry = tk.Entry(
            main_frame,
            font=("Segoe UI", 12),
            bg="#3a3a3a",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=28
        )
        self.value_entry.grid(row=1, column=1, padx=15, pady=15)

        # From unit
        ttk.Label(main_frame, text="From Unit:").grid(row=2, column=0, padx=15, pady=15, sticky="w")
        self.from_unit_var = tk.StringVar()
        self.from_unit_combo = ttk.Combobox(
            main_frame,
            textvariable=self.from_unit_var,
            state="readonly",
            width=25
        )
        self.from_unit_combo.grid(row=2, column=1, padx=15, pady=15)

        # To unit
        ttk.Label(main_frame, text="To Unit:").grid(row=3, column=0, padx=15, pady=15, sticky="w")
        self.to_unit_var = tk.StringVar()
        self.to_unit_combo = ttk.Combobox(
            main_frame,
            textvariable=self.to_unit_var,
            state="readonly",
            width=25
        )
        self.to_unit_combo.grid(row=3, column=1, padx=15, pady=15)

        # Convert button
        convert_btn = tk.Button(
            main_frame,
            text="Convert",
            command=self.convert_units,
            bg="#00d4ff",
            fg="black",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        convert_btn.grid(row=4, column=0, columnspan=2, pady=20)

        # Result label
        self.result_label = tk.Label(
            main_frame,
            text="Result: ",
            bg="#2b2b2b",
            fg="#00ff99",
            font=("Segoe UI", 16, "bold")
        )
        self.result_label.grid(row=5, column=0, columnspan=2, pady=20)

        # Footer
        footer = tk.Label(
            self.root,
            text="Built with Python + Tkinter",
            bg="#1e1e1e",
            fg="#aaaaaa",
            font=("Segoe UI", 10)
        )
        footer.pack(pady=10)

    def update_units(self):
        category = self.category_var.get()
        units = self.categories[category]

        self.from_unit_combo["values"] = units
        self.to_unit_combo["values"] = units

        if units:
            self.from_unit_var.set(units[0])
            self.to_unit_var.set(units[1] if len(units) > 1 else units[0])

        self.result_label.config(text="Result: ")

    def convert_units(self):
        try:
            value = float(self.value_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        category = self.category_var.get()
        from_unit = self.from_unit_var.get()
        to_unit = self.to_unit_var.get()

        try:
            result = self.convert(category, value, from_unit, to_unit)
            self.result_label.config(text=f"Result: {result:.6f} {to_unit}")
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def convert(self, category, value, from_unit, to_unit):
        if category == "Length":
            return self.convert_length(value, from_unit, to_unit)
        elif category == "Weight":
            return self.convert_weight(value, from_unit, to_unit)
        elif category == "Temperature":
            return self.convert_temperature(value, from_unit, to_unit)
        elif category == "Time":
            return self.convert_time(value, from_unit, to_unit)
        elif category == "Speed":
            return self.convert_speed(value, from_unit, to_unit)
        else:
            raise ValueError("Unsupported category selected.")

    def convert_length(self, value, from_unit, to_unit):
        to_meter = {
            "Meter": 1,
            "Kilometer": 1000,
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
            "Kilogram": 1,
            "Gram": 0.001,
            "Milligram": 0.000001,
            "Pound": 0.45359237,
            "Ounce": 0.028349523125,
        }
        kg = value * to_kg[from_unit]
        return kg / to_kg[to_unit]

    def convert_temperature(self, value, from_unit, to_unit):
        # Convert from source to Celsius
        if from_unit == "Celsius":
            celsius = value
        elif from_unit == "Fahrenheit":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        else:
            raise ValueError("Invalid temperature unit.")

        # Convert Celsius to target
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
            "Second": 1,
            "Minute": 60,
            "Hour": 3600,
            "Day": 86400,
        }
        seconds = value * to_second[from_unit]
        return seconds / to_second[to_unit]

    def convert_speed(self, value, from_unit, to_unit):
        to_mps = {
            "m/s": 1,
            "km/h": 0.2777777778,
            "mph": 0.44704,
        }
        mps = value * to_mps[from_unit]
        return mps / to_mps[to_unit]


if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverterApp(root)
    root.mainloop()
    