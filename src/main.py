#!/usr/bin/env python3
import sqlite3
import random

class TableAlreadyExistsError(Exception):
    pass

class ToDo:
    def __init__(self, table_name: str):
        with sqlite3.connect("tasks.db") as connection:
            cursor = connection.cursor()

            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                task TEXT,
                status INTEGER
            )""")
            
            connection.commit()

        self.table_name = table_name
    
    @staticmethod
    def generate_id(table_name: str) -> str:
        with sqlite3.connect("tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT id FROM {table_name}")
            ids = [id[0] for id in cursor.fetchall()]
            new_id = str(random.randint(1000, 9999))

            while new_id in ids:
                new_id = str(random.randint(1000, 9999))

            return new_id

    def add_task(self, task: str, status: bool = False) -> None:
        new_id = ToDo.generate_id(self.table_name)

        with sqlite3.connect("tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO {self.table_name} (id, task, status) VALUES (?, ?, ?)", (new_id, task, status))
            connection.commit()

    def delete_task(self, task_id: str) -> None:
        with sqlite3.connect("tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (task_id,))
            connection.commit()

    def change_status(self, task_id: str) -> None:
        with sqlite3.connect("tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT status FROM {self.table_name} WHERE id = ?", (task_id,))
            curr_status = cursor.fetchone()[0]

            new_status = not curr_status
            cursor.execute(f"UPDATE {self.table_name} SET status = ? WHERE id = ?", (new_status, task_id))

            connection.commit()
    
    def printTasks(self) -> None:
        # Connect to the database
        with sqlite3.connect("tasks.db") as connection:
            # Create a cursor object
            cursor = connection.cursor()

            # Execute a SELECT statement to fetch the table data
            cursor.execute("SELECT * FROM tasks")

            # Fetch all rows from the result
            rows = cursor.fetchall()

            # Get the column names
            column_names = [description[0] for description in cursor.description]

            # Print the column names
            print("\t".join(column_names))

            # Print the rows
            for row in rows:
                print("\t".join(str(value) for value in row))
    
    def clear_db(self) -> None:
        with sqlite3.connect("tasks.db") as connection:
            cursor = connection.cursor()

            cursor.execute(f"DELETE FROM {self.table_name}")

            connection.commit()

if __name__ == "__main__":
    obj1 = ToDo("tasks")
    obj1.clear_db()
    obj1.printTasks()

    obj2 = ToDo("running")
    obj2.clear_db()
    obj2.printTasks()
