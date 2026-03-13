import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from file_handler import load_file, save_file
from cleaner_engine import clean_dataframe


def start_app():
    app = ExcelCleanerGUI()
    app.root.mainloop()


class ExcelCleanerGUI:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Excel Cleaner")
        self.root.iconbitmap("excel_cleaner.ico")
        self.root.geometry("450x500")

        self.file_path = None

        title = tk.Label(self.root, text="Excel Cleaner", font=("Arial", 16))
        title.pack(pady=10)

        btn_select = tk.Button(self.root, text="Select File", command=self.select_file)
        btn_select.pack(pady=5)

        self.file_label = tk.Label(self.root, text="No file selected")
        self.file_label.pack(pady=5)

        preview_label = tk.Label(self.root, text="Preview (first 10 rows)")
        preview_label.pack(pady=5)

        preview_frame = tk.Frame(self.root)
        preview_frame.pack(pady=5)

        self.preview_table = ttk.Treeview(preview_frame, height=8)

        scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_table.yview)
        self.preview_table.configure(yscrollcommand=scrollbar.set)

        self.preview_table.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns")

        tk.Label(self.root, text="Cleaning").pack(pady=10)

        self.remove_duplicates = tk.BooleanVar()
        self.trim_spaces = tk.BooleanVar()
        self.remove_empty_rows = tk.BooleanVar()
        self.remove_empty_columns = tk.BooleanVar()

        tk.Checkbutton(self.root, text="Remove duplicate rows", variable=self.remove_duplicates).pack(anchor="w")
        tk.Checkbutton(self.root, text="Trim spaces", variable=self.trim_spaces).pack(anchor="w")
        tk.Checkbutton(self.root, text="Remove empty rows", variable=self.remove_empty_rows).pack(anchor="w")
        tk.Checkbutton(self.root, text="Remove empty columns", variable=self.remove_empty_columns).pack(anchor="w")

        tk.Label(self.root, text="Normalization").pack(pady=10)

        self.capitalize_names = tk.BooleanVar()
        self.lowercase_emails = tk.BooleanVar()
        self.normalize_phones = tk.BooleanVar()
        self.standardize_countries = tk.BooleanVar()
        self.standardize_dates = tk.BooleanVar()

        tk.Checkbutton(self.root, text="Capitalize names", variable=self.capitalize_names).pack(anchor="w")
        tk.Checkbutton(self.root, text="Lowercase emails", variable=self.lowercase_emails).pack(anchor="w")
        tk.Checkbutton(self.root, text="Normalize phone numbers", variable=self.normalize_phones).pack(anchor="w")
        tk.Checkbutton(self.root, text="Standardize country names", variable=self.standardize_countries).pack(anchor="w")
        tk.Checkbutton(self.root, text="Standardize date format", variable=self.standardize_dates).pack(anchor="w")

        tk.Label(self.root, text="Validation").pack(pady=10)

        self.validate_emails = tk.BooleanVar()

        tk.Checkbutton(self.root, text="Validate emails", variable=self.validate_emails).pack(anchor="w")

        clean_button = tk.Button(self.root, text="CLEAN DATA", command=self.clean_file)
        clean_button.pack(pady=20)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.status = tk.Label(self.root, text="Status: Waiting for file")
        self.status.pack(pady=10)

    def show_preview(self, df):

        # usuń stare dane
        for item in self.preview_table.get_children():
            self.preview_table.delete(item)

        self.preview_table["columns"] = list(df.columns)
        self.preview_table["show"] = "headings"

        for col in df.columns:
            self.preview_table.heading(col, text=col)
            self.preview_table.column(col, width=100)

        preview_rows = df.head(10).values

        for row in preview_rows:
            self.preview_table.insert("", "end", values=list(row))

    def select_file(self):

        filetypes = [
            ("Excel files", "*.xlsx *.xls"),
            ("CSV files", "*.csv")
        ]

        path = filedialog.askopenfilename(filetypes=filetypes)

        if path:
            self.file_path = path
            self.file_label.config(text=path)

            df = load_file(path)
            self.show_preview(df)

    def clean_file(self):

        if not self.file_path:
            messagebox.showerror("Error", "Select file first")
            return

        self.status.config(text="Status: Loading file...")
        self.root.update()

        df = load_file(self.file_path)

        options = {
            "remove_duplicates": self.remove_duplicates.get(),
            "trim_spaces": self.trim_spaces.get(),
            "remove_empty_rows": self.remove_empty_rows.get(),
            "remove_empty_columns": self.remove_empty_columns.get(),
            "capitalize_names": self.capitalize_names.get(),
            "lowercase_emails": self.lowercase_emails.get(),
            "normalize_phones": self.normalize_phones.get(),
            "standardize_countries": self.standardize_countries.get(),
            "standardize_dates": self.standardize_dates.get(),
            "validate_emails": self.validate_emails.get()
        }

        self.progress["value"] = 20
        self.status.config(text="Status: Cleaning data...")
        self.root.update()

        df, report = clean_dataframe(df, options)

        self.progress["value"] = 80
        self.status.config(text="Status: Saving file...")
        self.root.update()

        output_path = save_file(self.file_path, df)

        self.progress["value"] = 100
        self.status.config(text="Status: Cleaning complete")
        self.root.update()

        messagebox.showinfo("Done", report + f"\nSaved to:\n{output_path}")

       