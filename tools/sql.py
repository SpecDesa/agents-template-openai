import sqlite3
from pydantic.v1 import BaseModel # Annotate diff class in python. Clear describe expected. 
from typing import List 
from langchain.tools import Tool

# Database with ecommerce fake data
conn = sqlite3.connect("db.sqlite")


# List all tables
def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

# Function for llm to call
def run_sqlite_query(query):
    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occured {str(err)}"


# Basicly, if you want to be a class of this, 
# you need to provide a query attribute that is a string
class RunQueryArgsSchema(BaseModel):
    query: str

# Create tool.
# Langchain can use args_schema to better understand args.otherwise, 
# will be __arg1 internally.
run_query_tool = Tool.from_function(
        name="run_sqlite_query",
        # Be decise and direct
        description="Run a sqlite query",
        func=run_sqlite_query,
        args_schema=RunQueryArgsSchema
        )


# Take table names
def describe_tables(tables_names): 
    c = conn.cursor()
    # Concat list names
    tables = ', '.join("'"+ table + "'" for table in tables_names)
    rows = c.execute(f"SELECT sql from sqlite_master WHERE type='table' and name IN ({tables});")
    return '\n'.join(row[0] for row in rows if row[0] is not None)



class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

# Create it as a tool 
describe_tables_tool = Tool.from_function(
        name="describe_tables",
        description="Given a list of table names, return the schema of those tables.",
        func=describe_tables, 
        args_schema=DescribeTablesArgsSchema
        )
