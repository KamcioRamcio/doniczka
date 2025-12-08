import sqlite3
from pathlib import Path

def init_db(schema_path: str = "schema.sql") -> None:
    schema_file = Path(schema_path)
    if not schema_file.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_file}")

    sql = schema_file.read_text(encoding="utf-8")
    conn = sqlite3.connect("doniczka.db")
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()

