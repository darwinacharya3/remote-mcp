from fastmcp import FastMCP
import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("Expense Tracker")


def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )   
        """)

init_db()


@mcp.tool()
def add_expenses(date, amount, category, subcategory="", note=""):
    '''Add a new expense entry to the database'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status" : "OK", "id" : cur.lastrowid}


@mcp.tool()
def list_expenses(start_date, end_date):
    '''List all expenses in the database'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "SELECT id, date, amount, category, subcategory, note FROM expenses WHERE date BETWEEN ? AND ? ORDER BY id ASC", (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses in the database'''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) as total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]
        if category:
            query += "AND category = ?"
            params.append(category)
        
        query += "GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


@mcp.resource("expense://categories", "mine_type=application/json")
def categories():
    with open(CATEGORIES_PATH, "r", encoding="utf-") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)




















# from fastmcp import FastMCP
# import random
# import json

# # Create a FastMCP instance 
# mcp = FastMCP("Simple Calculator Server")

# # Tool: Add two number
# @mcp.tool
# def add(a:int, b:int) -> int:
#     '''Add two numbers together
#         Args:
#             a: First number
#             b: Second number
#         Returns:
#             Sum of a and b
    
#     '''
#     return a + b

# # tool to generate random number
# @mcp.tool
# def random_number(min_value: int = 1, max_value: int = 100) -> int:
#     '''Generate a random number between min_value and max_value
#         Args:
#             min_value: Minimum value of the range
#             max_value: Maximum value of the range
#         Returns:
#             Random number between min_value and max_value
#     '''
#     return random.randint(min_value, max_value) 


# # Resources: Server information
# @mcp.resource("info://server")
# def server_info() -> str:
#     '''Get information about this server'''
#     info = {
#         'name' : 'Simple Calculator Server',
#         'version' : '1.0.0',
#         'description' : 'A basic MCP server with math tools',
#         'tools' : ["add", "random_number"],
#         "author" : "Darwin Acharya"
#     }
#     return json.dumps(info, indent=2)


# # Start the server
# if __name__ == "__main__":
#     mcp.run(transport="http", host="0.0.0.0", port=8000)

