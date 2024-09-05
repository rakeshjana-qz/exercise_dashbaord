# This is deprecated in favor of the GUI application
# Use ui.py and csv_processor.py to implement the GUI application
# TODO: Remove this file after implementing the GUI application
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
from pathlib import Path
from utils import process_csv_and_add_encoded_query_string

class CSVLinkGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Link Generator")

        # Input CSV file with drag-and-drop capability
        self.input_label = tk.Label(root, text="Input CSV File:")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)

        # Enable drag-and-drop for the input entry field
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

        # Generate Button (Initially placed on the grid)
        self.generate_button = tk.Button(root, text="Generate", command=self.generate_files)
        self.generate_button.grid(row=3, column=0, columnspan=3, pady=20)    
    
    def set_output_and_log_paths(self, input_file):
        # Extract the directory from the input CSV file path
        input_dir = os.path.dirname(input_file)

        # Set the output and log file paths in the same directory as the input file
        output_csv = os.path.join(input_dir, "output.csv")
        log_csv = os.path.join(input_dir, "log.csv")

        # Update and display the output and log entry fields
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, output_csv)
        self.log_entry.delete(0, tk.END)
        self.log_entry.insert(0, log_csv)

        # Now place the output and log fields on the grid
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

            # Call the new method to set and display output and log paths
            self.set_output_and_log_paths(input_file)

    def drop_input_file(self, event):
        file_path = event.data

        # Remove curly braces if present
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]

        if file_path.lower().endswith('.csv'):
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)

            # Call the new method to set and display output and log paths
            self.set_output_and_log_paths(file_path)
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

    def generate_files(self):
        input_csv = self.input_entry.get()
        output_csv = self.output_entry.get()
        log_csv = self.log_entry.get()

        if not input_csv:
            messagebox.showerror("Error", "Please specify the input CSV file path.")
            return
        
        # Extract the directory from the input CSV file path
        input_dir = os.path.dirname(input_csv)

        # Set the output and log file paths in the same directory as the input file
        output_csv = os.path.join(input_dir, "output.csv")
        log_csv = os.path.join(input_dir, "log.csv")

        # Update the output and log entry fields with the new paths
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, output_csv)
        
        self.log_entry.delete(0, tk.END)
        self.log_entry.insert(0, log_csv)

        # Ensure output and log files exist
        if not os.path.exists(output_csv):
            with open(output_csv, 'w', newline='', encoding='utf-8') as f:
                pass  # Create an empty file

        if not os.path.exists(log_csv):
            with open(log_csv, 'w', newline='', encoding='utf-8') as f:
                pass  # Create an empty file

        try:
            # Call the processing function and get the counts
            processed_count, ignored_count = process_csv_and_add_encoded_query_string(input_csv, output_csv, log_csv)
            
            # Display the results in a message box
            messagebox.showinfo("Processing Complete", f"Rows processed: {processed_count}\nRows ignored: {ignored_count}")

            messagebox.showinfo("Success", f"Files generated successfully:\n\nOutput: {output_csv}")
        except ValueError as e:
            messagebox.showerror("Format Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Initialize TkinterDnD only once
    app = CSVLinkGeneratorApp(root)
    root.mainloop()