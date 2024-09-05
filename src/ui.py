# src/ui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import tempfile
import uuid
import csv
from csv_processor import process_csv_and_add_encoded_query_string, validate_csv_format

class CSVLinkGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Link Generator")

        self.search_field_keys = {
            "ex_limit", "questionified", "specific_ids", "textbook_chapters", 
            "textbook_isbns", "textbook_pages", "exclude_isbns", "verified", 
            "question_batches", "question_subjects", "question_owners"
        }

        # Input CSV file with drag-and-drop capability
        self.input_label = tk.Label(root, text="Input CSV File:")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)
        self.input_entry.drop_target_register(DND_FILES)
        self.input_entry.dnd_bind('<<Drop>>', self.drop_input_file)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_input_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        # Output CSV file (Initially hidden)
        self.output_label = tk.Label(root, text="Output CSV File:")
        self.output_entry = tk.Entry(root, width=50)
        self.save_button = tk.Button(root, text="Save As", command=self.save_output_file)

        # Log CSV file (Initially hidden)
        self.log_label = tk.Label(root, text="Log CSV File:")
        self.log_entry = tk.Entry(root, width=50)
        self.log_button = tk.Button(root, text="Save As", command=self.save_log_file)

        # Table for displaying CSV content
        self.table = ttk.Treeview(root)
        self.table.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.table_scroll = ttk.Scrollbar(root, orient="vertical", command=self.table.yview)
        self.table_scroll.grid(row=4, column=3, sticky='ns')
        self.table.configure(yscrollcommand=self.table_scroll.set)

        # Generate Button
        self.generate_button = tk.Button(root, text="Generate", command=self.generate_files)
        self.generate_button.grid(row=5, column=0, columnspan=3, pady=20)

    def set_output_and_log_paths(self, input_file):
        input_dir = os.path.dirname(input_file)
        output_csv = os.path.join(input_dir, "output.csv")
        log_csv = os.path.join(input_dir, "log.csv")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, output_csv)
        self.log_entry.delete(0, tk.END)
        self.log_entry.insert(0, log_csv)
        self.output_label.grid(row=1, column=0, padx=10, pady=10)
        self.output_entry.grid(row=1, column=1, padx=10, pady=10)
        self.save_button.grid(row=1, column=2, padx=10, pady=10)
        self.log_label.grid(row=2, column=0, padx=10, pady=10)
        self.log_entry.grid(row=2, column=1, padx=10, pady=10)
        self.log_button.grid(row=2, column=2, padx=10, pady=10)

    def browse_input_file(self):
        input_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if input_file:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_file)
            self.set_output_and_log_paths(input_file)
            self.display_csv_data(input_file)

    def drop_input_file(self, event):
        file_path = event.data
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]
        if file_path.lower().endswith('.csv'):
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
            self.set_output_and_log_paths(file_path)
            self.display_csv_data(file_path)
        else:
            messagebox.showerror("Invalid File", "Please drop a CSV file.")

    def save_output_file(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, output_file)

    def save_log_file(self):
        log_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        self.log_entry.delete(0, tk.END)
        self.log_entry.insert(0, log_file)

    def display_csv_data(self, input_file):
        try:
            data = validate_csv_format(input_file, self.search_field_keys)
            
            # Clear existing table data
            self.table.delete(*self.table.get_children())
            
            # Set table columns correctly
            self.table["columns"] = list(data[0].keys())  # Convert dict_keys to list
            self.table["show"] = "headings"  # Hide the first column which is an implicit row ID
            
            for col in self.table["columns"]:
                self.table.heading(col, text=col)
                self.table.column(col, width=100)
                
            self.csv_data = data  # Store data in an instance variable for later use
            
            for i, row in enumerate(data):
                self.table.insert("", "end", iid=i, values=list(row.values()))
            
            # Bind a double-click event to the Treeview to edit cells
            self.table.bind("<Double-1>", self.on_double_click)
            
            
        except ValueError as e:
            messagebox.showerror("Format Error", str(e))

    def on_double_click(self, event):
        # Identify the row and column where the double-click occurred
        region = self.table.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.table.identify_row(event.y)
            col_id = self.table.identify_column(event.x)
            col_index = int(col_id.replace("#", "")) - 1
            col_name = self.table["columns"][col_index]

            # Get current value
            old_value = self.table.item(row_id, "values")[col_index]

            # Get the cell bounding box to position the entry widget
            bbox = self.table.bbox(row_id, col_id)
            if not bbox:
                return
            x, y, width, height = bbox

            # Create an entry widget for the user to edit the cell value
            entry = tk.Entry(self.root)
            entry.insert(0, old_value)
            entry.select_range(0, tk.END)
            entry.focus()

            # Place the entry widget directly over the cell
            entry.place(x=x + self.table.winfo_x(), y=y + self.table.winfo_y(), width=width, height=height)

            # Bind the return key to update the cell and remove the entry widget
            entry.bind("<Return>", lambda e: self.update_cell_value(entry, row_id, col_name, old_value))
            entry.bind("<FocusOut>", lambda e: entry.destroy())  # Destroy entry on focus out        
            
    def update_cell_value(self, entry, row_id, col_name, old_value):
        new_value = entry.get()
        entry.destroy()

        # Update the displayed value in the Treeview
        self.table.set(row_id, col_name, new_value)

        # Update the stored data
        self.csv_data[int(row_id)][col_name] = new_value

        # Print debug info (optional)
        print(f"Updated row {row_id}, column '{col_name}' from '{old_value}' to '{new_value}'")
        
        # Destroy the entry widget to exit edit mode
        entry.destroy()
    
    def save_edited_csv_to_temp(self, temp_filename):
        # Save the edited CSV data to a temporary file
        with open(temp_filename, mode='w', newline='', encoding='utf-8') as tempfile:
            writer = csv.DictWriter(tempfile, fieldnames=self.csv_data[0].keys())
            writer.writeheader()
            for row in self.csv_data:
                writer.writerow(row)
                
    def generate_files(self):
        input_csv = self.input_entry.get()
        output_csv = self.output_entry.get()
        log_csv = self.log_entry.get()
        
        if not input_csv:
            messagebox.showerror("Error", "Please specify the input CSV file path.")
            return

        try:
            # Ensure output and log files exist
            if not os.path.exists(output_csv):
                with open(output_csv, 'w', newline='', encoding='utf-8') as f:
                    pass # Create an empty file

            if not os.path.exists(log_csv):
                with open(log_csv, 'w', newline='', encoding='utf-8') as f:
                    pass # Create an empty file

            # Use self.csv_data for processing
            # Generate a temporary file to store the edited CSV data
            temp_filename = os.path.join(tempfile.gettempdir(), f"temp-{uuid.uuid4().hex}.csv")
            self.save_edited_csv_to_temp(temp_filename)
            
            # Call the processing function and get the counts
            processed_count, ignored_count = process_csv_and_add_encoded_query_string(temp_filename, output_csv, log_csv, self.search_field_keys)

            # Display the results in a message box
            messagebox.showinfo("Processing Complete", f"Rows processed: {processed_count}\nRows ignored: {ignored_count}")

            # Display success message after processing
            messagebox.showinfo("Success", f"Files generated successfully:\n\nOutput: {output_csv}\nLog: {log_csv}")
        
        except ValueError as e:
            # Specific handling for ValueError exceptions
            messagebox.showerror("Format Error", f"Format error: {str(e)}")
        except Exception as e:
             # Catch all other exceptions
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")