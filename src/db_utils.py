"""
Database Utility Module for Aegis Intelligence Database (AID)
Handles connection management and query execution with proper error handling.
"""

import pymysql
import sys
from contextlib import contextmanager


class DatabaseConnection:
    """Manages database connections for the AID system."""
    
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        """Establishes a connection to the MySQL database."""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            print("[AID SYSTEM] Database connection established.")
            return True
        except pymysql.Error as e:
            print(f"[AID ERROR] Failed to connect to database: {e}", file=sys.stderr)
            return False
    
    def disconnect(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            print("[AID SYSTEM] Database connection closed.")
    
    def execute_query(self, sql, params=None):
        """
        Executes a SELECT query and returns results.
        
        Args:
            sql (str): The SQL query string
            params (tuple): Parameters for parameterized query
            
        Returns:
            list: List of dictionaries containing query results
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params or ())
                results = cursor.fetchall()
                return results
        except pymysql.Error as e:
            print(f"[AID ERROR] Query execution failed: {e}", file=sys.stderr)
            return None
    
    def execute_update(self, sql, params=None):
        """
        Executes an INSERT, UPDATE, or DELETE query.
        
        Args:
            sql (str): The SQL query string
            params (tuple): Parameters for parameterized query
            
        Returns:
            int: Number of affected rows, or -1 on error
        """
        try:
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(sql, params or ())
                self.connection.commit()
                return affected_rows
        except pymysql.Error as e:
            print(f"[AID ERROR] Update execution failed: {e}", file=sys.stderr)
            self.connection.rollback()
            return -1
    
    def execute_ddl(self, sql):
        """
        Executes a DDL command (DROP, TRUNCATE, ALTER).
        ADMIN ONLY - Used for structural database changes.
        
        Args:
            sql (str): The DDL SQL command
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
                return True
        except pymysql.Error as e:
            print(f"[AID ERROR] DDL execution failed: {e}", file=sys.stderr)
            self.connection.rollback()
            return False


def format_query_results(results, empty_message="INTELLIGENCE NOT FOUND"):
    """
    Formats query results for display.
    
    Args:
        results: Query results from execute_query
        empty_message: Message to display when no results found
        
    Returns:
        str: Formatted results or error message
    """
    if results is None:
        return "DATABASE ERROR: Query execution failed."
    
    if not results:
        return empty_message
    
    return results


def get_db_password():
    """
    Securely prompts for database password at application startup.
    
    Returns:
        str: The database password entered by user
    """
    import getpass
    print("\n" + "="*60)
    print("AEGIS INTELLIGENCE DATABASE - AUTHENTICATION REQUIRED")
    print("="*60)
    password = getpass.getpass("Enter MySQL Database Password: ")
    return password
