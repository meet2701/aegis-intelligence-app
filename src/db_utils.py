"""
Database Utility Module for Aegis Intelligence Database (AID)
Handles connection management and query execution using a SQLAlchemy
connection pool backed by PyMySQL. The external API of DatabaseConnection
is preserved so no changes are needed elsewhere in the application.
"""

import sys
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class DatabaseConnection:
    """
    Manages a SQLAlchemy Engine-based connection pool for the AID system.

    Pool configuration:
        pool_size=5       — up to 5 persistent connections kept alive
        max_overflow=10   — up to 10 additional connections under burst load
        pool_recycle=3600 — recycle connections after 1 hour to avoid stale sockets
        pool_pre_ping=True — validate connections before checkout (handles DB restarts)
    """

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self._engine = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> bool:
        """
        Creates the SQLAlchemy Engine and initialises the connection pool.
        A test connection is made to verify the credentials are correct.

        Returns:
            bool: True on success, False on failure.
        """
        try:
            url = (
                f"mysql+pymysql://{self.user}:{self.password}"
                f"@{self.host}/{self.database}?charset=utf8mb4"
            )
            self._engine = create_engine(
                url,
                pool_size=5,
                max_overflow=10,
                pool_recycle=3600,
                pool_pre_ping=True,
                # Return rows as dicts (mimics pymysql DictCursor behaviour)
                execution_options={"stream_results": False},
            )
            # Eagerly probe the pool so a bad password fails here, not later.
            with self._engine.connect() as probe:
                probe.execute(text("SELECT 1"))
            print("[AID SYSTEM] SQLAlchemy connection pool established.")
            print(
                f"[AID SYSTEM] Pool: size={5}, max_overflow={10}, "
                "recycle=3600s, pre_ping=True"
            )
            return True
        except SQLAlchemyError as e:
            print(
                f"[AID ERROR] Failed to initialise connection pool: {e}",
                file=sys.stderr,
            )
            return False

    def disconnect(self):
        """Disposes the engine, closing all pooled connections."""
        if self._engine:
            self._engine.dispose()
            print("[AID SYSTEM] Connection pool disposed.")

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def execute_query(self, sql: str, params=None) -> list | None:
        """
        Executes a SELECT query and returns results as a list of dicts.

        Each call checks out a connection from the pool and automatically
        returns it on exit (context-manager pattern).

        Args:
            sql (str): The SQL query string (use %s placeholders).
            params (tuple | None): Bound parameters for the query.

        Returns:
            list[dict] | None: Rows as dicts, or None on error.
        """
        try:
            # Convert %s placeholders to SQLAlchemy :param style
            bound_sql, bound_params = _prepare(sql, params)
            with self._engine.connect() as conn:
                result = conn.execute(text(bound_sql), bound_params)
                keys = result.keys()
                rows = [dict(zip(keys, row)) for row in result.fetchall()]
                return rows
        except SQLAlchemyError as e:
            print(f"[AID ERROR] Query execution failed: {e}", file=sys.stderr)
            return None

    def execute_update(self, sql: str, params=None) -> int:
        """
        Executes an INSERT, UPDATE, or DELETE query within a transaction.

        The transaction is automatically committed on success and rolled
        back on any exception.

        Args:
            sql (str): The SQL statement (use %s placeholders).
            params (tuple | None): Bound parameters.

        Returns:
            int: Number of affected rows, or -1 on error.
        """
        try:
            bound_sql, bound_params = _prepare(sql, params)
            with self._engine.begin() as conn:          # auto-commit / rollback
                result = conn.execute(text(bound_sql), bound_params)
                return result.rowcount
        except SQLAlchemyError as e:
            print(f"[AID ERROR] Update execution failed: {e}", file=sys.stderr)
            return -1

    def execute_ddl(self, sql: str) -> bool:
        """
        Executes a DDL command (DROP, TRUNCATE, ALTER, SET, SHOW …).
        ADMIN ONLY — Used for structural database changes.

        Args:
            sql (str): The raw DDL / admin SQL command.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with self._engine.begin() as conn:
                conn.execute(text(sql))
            return True
        except SQLAlchemyError as e:
            print(f"[AID ERROR] DDL execution failed: {e}", file=sys.stderr)
            return False


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _prepare(sql: str, params) -> tuple[str, dict]:
    """
    Converts a PyMySQL-style query (positional %s placeholders) into the
    named-parameter format expected by SQLAlchemy's text() construct.

    Example:
        "SELECT * FROM T WHERE id = %s AND name = %s", (1, 'Luffy')
        → "SELECT * FROM T WHERE id = :p0 AND name = :p1", {'p0': 1, 'p1': 'Luffy'}
    """
    if not params:
        return sql, {}

    param_dict: dict = {}
    converted = sql
    for i, value in enumerate(params):
        key = f"p{i}"
        # Replace only the first remaining %s each iteration
        converted = converted.replace("%s", f":{key}", 1)
        param_dict[key] = value

    return converted, param_dict


# ---------------------------------------------------------------------------
# Public utility functions (unchanged API)
# ---------------------------------------------------------------------------

def format_query_results(results, empty_message="INTELLIGENCE NOT FOUND"):
    """
    Formats query results for display.

    Args:
        results: Query results from execute_query
        empty_message: Message to display when no results found

    Returns:
        str | list: Formatted results or error message string
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
    print("\n" + "=" * 60)
    print("AEGIS INTELLIGENCE DATABASE - AUTHENTICATION REQUIRED")
    print("=" * 60)
    password = getpass.getpass("Enter MySQL Database Password: ")
    return password
