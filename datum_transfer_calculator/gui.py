import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox

import pandas as pd

from datum_transfer_calculator.core import (
    get_low_columns,
    get_high,
    calculate_ranges_and_means,
    calculate_sound_datum,
)


class DatumTransferCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.build_ui()
        self.mount_ui()

    def build_ui(self):
        self.title("Datum Transfer Calculator")

        self.label_for_file1 = tk.Label(self, text="Select Secondary Port:")

        self.entry_for_file1 = tk.Entry(self, width=50)

        self.browse_button_for_file1 = tk.Button(
            self, text="Browse", command=lambda: self.browse_files(self.entry_for_file1)
        )

        self.label_for_file2 = tk.Label(self, text="Select Standard Port:")

        self.entry_for_file2 = tk.Entry(self, width=50)

        self.browse_button_for_file2 = tk.Button(
            self, text="Browse", command=lambda: self.browse_files(self.entry_for_file2)
        )

        self.calcualte_button = tk.Button(
            self,
            text="Run",
            command=lambda: self.on_execute_button(
                self.entry_for_file1, self.entry_for_file2, self
            ),
        )

        self.author_info = tk.Label(
            self,
            text="Datum Transfer Calculator by Group 1",
            font=("Calibri", 14, "bold"),
            fg="black",
        )

    def mount_ui(self):
        self.label_for_file1.grid(row=0, column=0, padx=10, pady=10)
        self.entry_for_file1.grid(row=0, column=1, padx=10, pady=10)
        self.browse_button_for_file1.grid(row=0, column=2, padx=10, pady=10)
        self.label_for_file2.grid(row=1, column=0, padx=10, pady=10)
        self.entry_for_file2.grid(row=1, column=1, padx=10, pady=10)
        self.browse_button_for_file2.grid(row=1, column=2, padx=10, pady=10)
        self.calcualte_button.grid(row=2, column=1, pady=20)
        self.author_info.grid(row=3, column=0, columnspan=3)

    def run(self):
        self.mainloop()

    def operation_trigger(self, file1_path: str, file2_path: str):
        """Triggers the get low, get high and sound datum after reading the data in the uploaded files."""
        dataframe_1 = pd.read_csv(file1_path)
        dataframe_2 = pd.read_csv(file2_path)

        try:
            low_columns_1 = get_low_columns(dataframe_1["LW"])
        except KeyError:
            messagebox.showwarning(
                "Error", "Please, make sure low water column is in file 1."
            )

        try:
            low_columns_2 = get_low_columns(dataframe_2["LW"])
        except KeyError:
            messagebox.showwarning(
                "Error", "Please, make sure low water column is in file 2."
            )

        try:
            high_columns_1 = get_high(dataframe_1["HW"])
        except KeyError:
            messagebox.showwarning(
                "Error", "Please, make sure high water column is in file 1."
            )

        try:
            high_columns_2 = get_high(dataframe_2["HW"])
        except KeyError:
            messagebox.showwarning(
                "Error", "Please, make sure high water column is in file 2."
            )

        low_ranges, low_means = calculate_ranges_and_means(
            low_columns_1, high_columns_1
        )
        high_ranges, high_means = calculate_ranges_and_means(
            low_columns_2, high_columns_2
        )

        new_gauge_sounding_datum = calculate_sound_datum(
            low_ranges, low_means, high_ranges, high_means
        )

        new_gauge_sounding_datum = [round(i, 2) for i in new_gauge_sounding_datum]

        return new_gauge_sounding_datum, low_ranges, low_means, high_ranges, high_means

    def browse_files(self, entry_widget: tk.Entry):
        """Browse the computer file system for the files to be uploaded

        Files allowed for upload are restricted to only CSV files.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

    def execute_operation(self, file1_path: str, file2_path: str):
        """
        Function responsible for displaying a preview
        after computing before saving to file on a system.
        """
        (
            new_gauge_sounding_datum,
            low_ranges,
            low_means,
            high_ranges,
            high_means,
        ) = self.operation_trigger(file1_path, file2_path)

        results = pd.DataFrame(
            {
                "Tidal Range at Secondary Port (m)": low_ranges,
                "MTL_Secondary (m)": low_means,
                "Tidal Range at Established Gauge/Port (m)": high_ranges,
                "MTL_Established (m)": high_means,
                "New Gauge Sounding Datum (m)": new_gauge_sounding_datum,
            }
        )  # converting to a pandas Dataframe
        result_dialog = tk.Toplevel(self)
        result_dialog.title("New Gauge Sounding Datum")
        # result_label = tk.Label(result_dialog, text="New Sounding Datum:\n" + str(results))
        # result_label.pack()
        tree = ttk.Treeview(result_dialog, columns=results.columns, show="headings")
        num = 0
        for col in results.columns:
            tree.heading(num, text=col)
            num += 1

        for index, row in results.iterrows():
            values = [str(row[col]) for col in results.columns]
            tree.insert("", "end", values=values)

        tree.pack(expand=True, fill="both")
        save_button = tk.Button(
            result_dialog,
            text="Save Result as CSV",
            command=lambda: self.save_result_as_csv(results),
        )
        save_button.pack()

    def save_result_as_csv(self, results):
        """
        Function to save a computing result to file on a system.
        """
        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        results.to_csv(save_path, index=False)  # saves to a csv file
        tk.messagebox.showinfo("Show Successful", "Result saved successfully as CSV.")

    def on_execute_button(self, entry_file1: tk.Entry, entry_file2: tk.Entry):
        """
        Function to trigger getting of files from the system.
        """
        file1_path = entry_file1.get()
        file2_path = entry_file2.get()

        if file1_path and file2_path:
            self.execute_operation(file1_path, file2_path)
        else:
            messagebox.showwarning("Error", "Please. select both CSV files.")
