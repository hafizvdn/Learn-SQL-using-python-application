# Simple SQL Desktop App

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A beginner-friendly desktop application built with Python. This tool is designed to help users learn and practice foundational SQL queries in a simple, self-contained environment.

![A screenshot of the Simple SQL Desktop App, showing a query 'select * from products' and the resulting table with 5 rows of data.](https://i.imgur.com/8m4nJt3.png)

## 🎯 Purpose

This project provides a hands-on sandbox for anyone new to SQL. It removes the complexity of setting up a full-scale database server (like MySQL or PostgreSQL) and allows you to immediately start writing queries, viewing results, and understanding how data is manipulated.

## ✨ Key Features

* **In-Memory Database:** Instantly load a "Sample DB" to start querying without any setup.
* **File-Based Database:** Create a new, persistent SQLite database or open an existing `.db` or `.sqlite` file.
* **SQL Query Executor:** A multi-line text editor to write and execute any standard SQL commands (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE TABLE`, etc.).
* **Results Viewer:** View query results in a clean, scrollable table format.
* **Sample Queries:** Load pre-written queries to demonstrate SQL syntax.
* **CSV Export:** Export the results of your `SELECT` queries to a `.csv` file with a single click.
* **Clear Feedback:** A status bar informs you if your query was successful and how many rows were returned or affected.

## 🛠️ Technologies Used

* **Python:** The core application logic.
* **Tkinter:** (Assumed) The built-in Python library for the graphical user interface (GUI).
* **SQLite:** The built-in `sqlite3` module is used as the database engine, allowing for both in-memory and file-based databases.

---

## 🚀 Getting Started

### Prerequisites

* [Python 3.9](https://www.python.org/downloads/) or newer.

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/simple-sql-app.git](https://github.com/your-username/simple-sql-app.git)
    cd simple-sql-app
    ```

2.  **Create a virtual environment (Recommended):**
    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Run the application:**
    (Since this project likely uses built-in libraries like `tkinter` and `sqlite3`, no external dependencies may be needed.)
    ```bash
    python main.py 
    ```
    *(Assuming the main script is `main.py`)*

---

## 📖 How to Use

1.  Launch the application by running `python main.py`.
2.  Click **"Sample DB"** to load the default `products` table into memory.
3.  In the "SQL Query" box, type a query. Try one of these:
    * `SELECT * FROM products WHERE category = 'Furniture'`
    * `SELECT name, price FROM products ORDER BY price DESC`
    * `SELECT category, COUNT(*) FROM products GROUP BY category`
4.  Click **"Execute"** to run the query.
5.  View the output in the "Results" panel.
6.  Click **"Export to CSV"** to save the current results to a file.
7.  Click **"Clear"** to empty the query box and results panel.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features (like syntax highlighting or query history), please feel free to fork the repository and submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

This project is distributed under the MIT License. See `LICENSE.txt` for more information.
