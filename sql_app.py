import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sqlite3
import csv
import os
from pathlib import Path

class SQLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple SQL Desktop App")
        self.root.geometry("1000x700")
        
        # Current database connection
        self.conn = None
        self.db_path = None
        
        self.create_widgets()
        
        # Create a default in-memory database with sample data
        self.create_sample_database()
        
    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Database section
        db_frame = ttk.LabelFrame(main_frame, text="Database", padding="5")
        db_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        db_frame.columnconfigure(1, weight=1)
        
        ttk.Button(db_frame, text="New DB", command=self.new_database).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(db_frame, text="Open DB", command=self.open_database).grid(row=0, column=1, padx=5)
        ttk.Button(db_frame, text="Sample DB", command=self.create_sample_database).grid(row=0, column=2, padx=5)
        
        self.db_label = ttk.Label(db_frame, text="Current: In-Memory Sample Database")
        self.db_label.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Query section
        query_frame = ttk.LabelFrame(main_frame, text="SQL Query", padding="5")
        query_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        query_frame.columnconfigure(0, weight=1)
        
        # Query text area
        self.query_text = scrolledtext.ScrolledText(query_frame, height=6, wrap=tk.WORD)
        self.query_text.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Query buttons
        ttk.Button(query_frame, text="Execute", command=self.execute_query).grid(row=1, column=0, padx=(0, 5))
        ttk.Button(query_frame, text="Clear", command=self.clear_query).grid(row=1, column=1, padx=5)
        ttk.Button(query_frame, text="Sample Queries", command=self.show_sample_queries).grid(row=1, column=2, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="5")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Create Treeview for results
        self.tree = ttk.Treeview(results_frame)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars for the tree
        v_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Export button
        ttk.Button(results_frame, text="Export to CSV", command=self.export_results).grid(row=2, column=0, pady=(5, 0))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def new_database(self):
        """Create a new SQLite database"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite files", "*.db"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if self.conn:
                    self.conn.close()
                
                self.conn = sqlite3.connect(file_path)
                self.db_path = file_path
                self.db_label.config(text=f"Current: {os.path.basename(file_path)}")
                self.status_var.set(f"Created new database: {os.path.basename(file_path)}")
                self.clear_results()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create database: {str(e)}")
    
    def open_database(self):
        """Open an existing SQLite database"""
        file_path = filedialog.askopenfilename(
            filetypes=[("SQLite files", "*.db"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if self.conn:
                    self.conn.close()
                
                self.conn = sqlite3.connect(file_path)
                self.db_path = file_path
                self.db_label.config(text=f"Current: {os.path.basename(file_path)}")
                self.status_var.set(f"Opened database: {os.path.basename(file_path)}")
                self.clear_results()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open database: {str(e)}")
    
    def create_sample_database(self):
        """Create a sample in-memory database with test data"""
        try:
            if self.conn:
                self.conn.close()
            
            self.conn = sqlite3.connect(":memory:")
            self.db_path = ":memory:"
            
            # Create sample tables
            cursor = self.conn.cursor()
            
            # Employees table
            cursor.execute("""
                CREATE TABLE employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    salary REAL,
                    hire_date DATE
                )
            """)
            
            # Products table
            cursor.execute("""
                CREATE TABLE products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL,
                    stock INTEGER
                )
            """)
            
            # Insert sample data
            employees_data = [
                (1, 'Alice Johnson', 'Engineering', 85000, '2022-01-15'),
                (2, 'Bob Smith', 'Sales', 60000, '2021-03-20'),
                (3, 'Carol Davis', 'Engineering', 90000, '2020-07-10'),
                (4, 'David Wilson', 'Marketing', 55000, '2023-02-28'),
                (5, 'Eve Brown', 'Sales', 65000, '2022-11-05')
            ]
            
            products_data = [
                (1, 'Laptop Pro', 'Electronics', 1299.99, 25),
                (2, 'Wireless Mouse', 'Electronics', 29.99, 150),
                (3, 'Office Chair', 'Furniture', 299.99, 40),
                (4, 'Desk Lamp', 'Furniture', 79.99, 60),
                (5, 'USB-C Cable', 'Electronics', 19.99, 200)
            ]
            
            cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees_data)
            cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", products_data)
            
            self.conn.commit()
            self.db_label.config(text="Current: In-Memory Sample Database")
            self.status_var.set("Sample database created with employees and products tables")
            self.clear_results()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create sample database: {str(e)}")
    
    def execute_query(self):
        """Execute the SQL query"""
        if not self.conn:
            messagebox.showwarning("Warning", "No database connected")
            return
        
        query = self.query_text.get(1.0, tk.END).strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a query")
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            
            # Check if it's a SELECT query or other
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                self.display_results(results, columns)
                self.status_var.set(f"Query executed successfully. {len(results)} rows returned.")
            else:
                self.conn.commit()
                rows_affected = cursor.rowcount
                self.clear_results()
                self.status_var.set(f"Query executed successfully. {rows_affected} rows affected.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {str(e)}")
            self.status_var.set("Query failed")
    
    def display_results(self, results, columns):
        """Display query results in the treeview"""
        self.clear_results()
        
        # Configure columns
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        # Configure column headings and widths
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, minwidth=50)
        
        # Insert data
        for row in results:
            self.tree.insert("", "end", values=row)
    
    def clear_results(self):
        """Clear the results treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree["columns"] = ()
        self.tree["show"] = "tree"
    
    def clear_query(self):
        """Clear the query text area"""
        self.query_text.delete(1.0, tk.END)
    
    def show_sample_queries(self):
        """Show a window with sample queries"""
        sample_window = tk.Toplevel(self.root)
        sample_window.title("Sample Queries")
        sample_window.geometry("600x400")
        
        queries_text = scrolledtext.ScrolledText(sample_window, wrap=tk.WORD)
        queries_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        sample_queries = """Sample SQL Queries:

-- View all employees
SELECT * FROM employees;

-- View all products
SELECT * FROM products;

-- Find employees with salary > 70000
SELECT name, department, salary 
FROM employees 
WHERE salary > 70000;

-- Count employees by department
SELECT department, COUNT(*) as employee_count 
FROM employees 
GROUP BY department;

-- Products with low stock (< 50)
SELECT name, stock 
FROM products 
WHERE stock < 50;

-- Average salary by department
SELECT department, AVG(salary) as avg_salary 
FROM employees 
GROUP BY department;

-- Most expensive products
SELECT name, price 
FROM products 
ORDER BY price DESC 
LIMIT 3;

-- Insert new employee
INSERT INTO employees (name, department, salary, hire_date) 
VALUES ('John Doe', 'IT', 75000, '2024-01-01');

-- Update product price
UPDATE products 
SET price = 24.99 
WHERE name = 'USB-C Cable';

-- Delete employee by ID
DELETE FROM employees WHERE id = 5;
"""
        
        queries_text.insert(1.0, sample_queries)
        queries_text.config(state=tk.DISABLED)
    
    def export_results(self):
        """Export current results to CSV"""
        if not self.tree.get_children():
            messagebox.showwarning("Warning", "No results to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write headers
                    headers = [self.tree.heading(col)["text"] for col in self.tree["columns"]]
                    writer.writerow(headers)
                    
                    # Write data
                    for item in self.tree.get_children():
                        writer.writerow(self.tree.item(item)["values"])
                
                self.status_var.set(f"Results exported to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Results exported to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

def main():
    root = tk.Tk()
    app = SQLApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()