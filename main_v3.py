import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math


class ProUnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Unit Converter + Calculator")
        self.root.geometry("1080x700")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#0b1220")

        self.history = []

        self.categories = {
            "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"],
            "Weight": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Time": ["Second", "Minute", "Hour", "Day"],
            "Speed": ["m/s", "km/h", "mph"],
            "Area": ["Square Meter", "Square Kilometer", "Square Foot", "Square Inch", "Acre", "Hectare"],
            "Volume": ["Liter", "Milliliter", "Cubic Meter", "Cubic Centimeter", "Gallon"],
        }

        self.setup_styles()
        self.build_ui()
        self.update_units()

        self.root.bind("<Return>", self.handle_enter)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background="#0b1220", borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background="#1e293b",
            foreground="white",
            padding=(20, 10),
            font=("Segoe UI", 11, "bold")
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#38bdf8")],
            foreground=[("selected", "black")]
        )

        style.configure("TCombobox", padding=8, font=("Segoe UI", 11))
        style.configure("TLabel", background="#0b1220", foreground="white", font=("Segoe UI", 11))
        style.configure("Title.TLabel", background="#0b1220", foreground="#38bdf8", font=("Segoe UI", 24, "bold"))
        style.configure("Sub.TLabel", background="#0b1220", foreground="#94a3b8", font=("Segoe UI", 10))

    def build_ui(self):
        header = tk.Frame(self.root, bg="#0b1220")
        header.pack(fill="x", padx=20, pady=(15, 5))

        ttk.Label(header, text="Pro Unit Converter + Calculator", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Live conversion, scientific units, history saving, and calculator in one app.",
            style="Sub.TLabel"
        ).pack(anchor="w", pady=(4, 0))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=15)

        self.converter_tab = tk.Frame(self.notebook, bg="#0b1220")
        self.calculator_tab = tk.Frame(self.notebook, bg="#0b1220")

        self.notebook.add(self.converter_tab, text="Unit Converter")
        self.notebook.add(self.calculator_tab, text="Calculator")

        self.build_converter_tab()
        self.build_calculator_tab()

    def build_converter_tab(self):
        content = tk.Frame(self.converter_tab, bg="#0b1220")
        content.pack(fill="both", expand=True)
 
        left = tk.Frame(content, bg="#1e293b")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(content, bg="#1e293b", width=320)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self.build_converter_panel(left)
        self.build_history_panel(right)

    def build_converter_panel(self, parent):
        tk.Label(
            parent,
            text="Converter Dashboard",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        form = tk.Frame(parent, bg="#1e293b")
        form.pack(fill="both", expand=True, padx=20, pady=10)

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

        tk.Label(form, text="Enter Value", bg="#1e293b", fg="#cbd5e1", font=("Segoe UI", 11)).grid(
            row=0, column=1, sticky="w", pady=(5, 8)
        )
        self.value_var = tk.StringVar()
        self.value_entry = tk.Entry(
            form,
            textvariable=self.value_var,
            font=("Segoe UI", 12),
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.value_entry.grid(row=1, column=1, sticky="ew", pady=(0, 15))
        self.value_entry.bind("<KeyRelease>", lambda e: self.live_convert())

        tk.Label(form, text="From Unit", bg="#1e293b", fg="#cbd5e1", font=("Segoe UI", 11)).grid(
            row=2, column=0, sticky="w", pady=(5, 8)
        )
        self.from_var = tk.StringVar()
        self.from_combo = ttk.Combobox(form, textvariable=self.from_var, state="readonly", width=28)
        self.from_combo.grid(row=3, column=0, sticky="ew", padx=(0, 12), pady=(0, 15))
        self.from_combo.bind("<<ComboboxSelected>>", lambda e: self.live_convert())

        tk.Label(form, text="To Unit", bg="#1e293b", fg="#cbd5e1", font=("Segoe UI", 11)).grid(
            row=2, column=1, sticky="w", pady=(5, 8)
        )
        self.to_var = tk.StringVar()
        self.to_combo = ttk.Combobox(form, textvariable=self.to_var, state="readonly", width=28)
        self.to_combo.grid(row=3, column=1, sticky="ew", pady=(0, 15))
        self.to_combo.bind("<<ComboboxSelected>>", lambda e: self.live_convert())

        btn_row1 = tk.Frame(form, bg="#1e293b")
        btn_row1.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 10))

        self.make_button(btn_row1, "Convert", self.convert_units, "#38bdf8", "black").pack(side="left", padx=(0, 10))
        self.make_button(btn_row1, "Swap", self.swap_units, "#22c55e", "black").pack(side="left", padx=(0, 10))
        self.make_button(btn_row1, "Copy Result", self.copy_result, "#a78bfa", "black").pack(side="left", padx=(0, 10))
        self.make_button(btn_row1, "Clear All", self.clear_fields, "#f59e0b", "black").pack(side="left")

        btn_row2 = tk.Frame(form, bg="#1e293b")
        btn_row2.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        self.make_button(btn_row2, "Save History", self.save_history_to_file, "#ef4444", "white").pack(side="left")

        result_card = tk.Frame(form, bg="#0f172a")
        result_card.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 8))

        tk.Label(result_card, text="Live Result", bg="#0f172a", fg="#94a3b8", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=15, pady=(12, 5)
        )

        self.result_var = tk.StringVar(value="No conversion yet")
        self.result_label = tk.Label(
            result_card,
            textvariable=self.result_var,
            bg="#0f172a",
            fg="#22c55e",
            font=("Segoe UI", 20, "bold"),
            wraplength=580,
            justify="left"
        )
        self.result_label.pack(anchor="w", padx=15, pady=(0, 15))

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

    def build_history_panel(self, parent):
        tk.Label(parent, text="History", bg="#1e293b", fg="white", font=("Segoe UI", 18, "bold")).pack(
            anchor="w", padx=15, pady=(20, 10)
        )
        tk.Label(parent, text="Recent conversions with time", bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 10)).pack(
            anchor="w", padx=15, pady=(0, 10)
        )

        self.history_listbox = tk.Listbox(
            parent,
            bg="#0f172a",
            fg="white",
            font=("Consolas", 10),
            relief="flat",
            highlightthickness=0,
            selectbackground="#38bdf8",
            selectforeground="black"
        )
        self.history_listbox.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.make_button(parent, "Clear History", self.clear_history, "#dc2626", "white").pack(
            fill="x", padx=15, pady=(0, 15)
        )

    def build_calculator_tab(self):
        wrapper = tk.Frame(self.calculator_tab, bg="#0b1220")
        wrapper.pack(fill="both", expand=True, padx=20, pady=20)

        calc_frame = tk.Frame(wrapper, bg="#1e293b")
        calc_frame.pack(fill="both", expand=True)

        tk.Label(
            calc_frame,
            text="Calculator",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        self.calc_var = tk.StringVar()
        self.calc_entry = tk.Entry(
            calc_frame,
            textvariable=self.calc_var,
            font=("Segoe UI", 20),
            bg="#0f172a",
            fg="white",
            insertbackground="white",
            relief="flat",
            justify="right"
        )
        self.calc_entry.pack(fill="x", padx=20, pady=(0, 15), ipady=12)
        self.calc_entry.bind("<Return>", lambda e: self.calculate_expression())

        self.calc_result_var = tk.StringVar(value="Result: ")
        tk.Label(
            calc_frame,
            textvariable=self.calc_result_var,
            bg="#1e293b",
            fg="#22c55e",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=20, pady=(0, 15))

        buttons_frame = tk.Frame(calc_frame, bg="#1e293b")
        buttons_frame.pack(padx=20, pady=10)

        buttons = [
            ["7", "8", "9", "/", "sin"],
            ["4", "5", "6", "*", "cos"],
            ["1", "2", "3", "-", "tan"],
            ["0", ".", "(", ")", "+"],
            ["sqrt", "log", "pi", "C", "="],
        ]

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                action = lambda x=text: self.on_calc_button_click(x)
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    command=action,
                    width=8,
                    height=2,
                    bg="#334155",
                    fg="white",
                    activebackground="#38bdf8",
                    activeforeground="black",
                    relief="flat",
                    font=("Segoe UI", 12, "bold"),
                    cursor="hand2"
                )
                btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

        for i in range(5):
            buttons_frame.grid_columnconfigure(i, weight=1)

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
        self.live_convert()

    def handle_enter(self, event):
        if self.notebook.index(self.notebook.select()) == 0:
            self.convert_units()
        else:
            self.calculate_expression()

    def swap_units(self):
        a = self.from_var.get()
        b = self.to_var.get()
        self.from_var.set(b)
        self.to_var.set(a)
        self.live_convert()

    def clear_fields(self):
        self.value_var.set("")
        self.result_var.set("No conversion yet")
        self.value_entry.focus()

    def clear_history(self):
        self.history.clear()
        self.history_listbox.delete(0, tk.END)

    def copy_result(self):
        text = self.result_var.get()
        if text == "No conversion yet":
            messagebox.showwarning("Nothing to Copy", "Please perform a conversion first.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        messagebox.showinfo("Copied", "Result copied to clipboard.")

    def save_history_to_file(self):
        if not self.history:
            messagebox.showwarning("No History", "No conversion history to save.")
            return

        try:
            with open("history.txt", "a", encoding="utf-8") as file:
                file.write("\n===== Saved on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " =====\n")
                for item in self.history:
                    file.write(item + "\n")
            messagebox.showinfo("Saved", "History saved to history.txt")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def live_convert(self):
        raw_value = self.value_var.get().strip()
        if not raw_value:
            self.result_var.set("No conversion yet")
            return
        try:
            value = float(raw_value)
            result = self.convert(self.category_var.get(), value, self.from_var.get(), self.to_var.get())
            self.result_var.set(f"{self.format_number(value)} {self.from_var.get()} = {self.format_number(result)} {self.to_var.get()}")
        except Exception:
            self.result_var.set("Enter a valid number")

    def convert_units(self):
        raw_value = self.value_var.get().strip()

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
            text = f"{self.format_number(value)} {from_unit} = {self.format_number(result)} {to_unit}"
            self.result_var.set(text)
            self.add_to_history(text)
        except Exception as error:
            messagebox.showerror("Conversion Error", str(error))

    def add_to_history(self, text):
        stamp = datetime.now().strftime("%H:%M:%S")
        final_text = f"[{stamp}] {text}"
        self.history.append(final_text)
        self.history_listbox.insert(tk.END, final_text)

    def format_number(self, value):
        if abs(value) >= 1e6 or (0 < abs(value) < 1e-4):
            return f"{value:.6e}"
        return f"{value:.6f}".rstrip("0").rstrip(".")

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
        if category == "Area":
            return self.convert_area(value, from_unit, to_unit)
        if category == "Volume":
            return self.convert_volume(value, from_unit, to_unit)
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

    def convert_area(self, value, from_unit, to_unit):
        to_sq_meter = {
            "Square Meter": 1.0,
            "Square Kilometer": 1_000_000.0,
            "Square Foot": 0.09290304,
            "Square Inch": 0.00064516,
            "Acre": 4046.8564224,
            "Hectare": 10000.0,
        }
        sqm = value * to_sq_meter[from_unit]
        return sqm / to_sq_meter[to_unit]

    def convert_volume(self, value, from_unit, to_unit):
        to_liter = {
            "Liter": 1.0,
            "Milliliter": 0.001,
            "Cubic Meter": 1000.0,
            "Cubic Centimeter": 0.001,
            "Gallon": 3.785411784,
        }
        liters = value * to_liter[from_unit]
        return liters / to_liter[to_unit]

    def on_calc_button_click(self, text):
        if text == "C":
            self.calc_var.set("")
            self.calc_result_var.set("Result: ")
        elif text == "=":
            self.calculate_expression()
        elif text == "sin":
            self.calc_var.set(self.calc_var.get() + "sin(")
        elif text == "cos":
            self.calc_var.set(self.calc_var.get() + "cos(")
        elif text == "tan":
            self.calc_var.set(self.calc_var.get() + "tan(")
        elif text == "sqrt":
            self.calc_var.set(self.calc_var.get() + "sqrt(")
        elif text == "log":
            self.calc_var.set(self.calc_var.get() + "log10(")
        elif text == "pi":
            self.calc_var.set(self.calc_var.get() + "pi")
        else:
            self.calc_var.set(self.calc_var.get() + text)

    def calculate_expression(self):
        expression = self.calc_var.get().strip()

        if not expression:
            messagebox.showwarning("Empty", "Please enter an expression.")
            return

        safe_dict = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "log10": math.log10,
            "pi": math.pi,
            "e": math.e,
            "__builtins__": {}
        }

        try:
            result = eval(expression, safe_dict, {})
            self.calc_result_var.set(f"Result: {self.format_number(result)}")
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ProUnitConverter(root)
    root.mainloop()