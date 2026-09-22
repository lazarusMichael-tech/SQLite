from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"
SCHEMA = BASE_DIR / "schema.sql"

seed_students = [
    (19595, "Mr.narupa tapung non"),
    (46664, "Mr.patchaya Khunm cee"),
    (46677, "Mr.Michael ODanie Michael"),
    (46707, "Mr.Supawit duangnern tom"),
    (46746, "Mr.Jirayu pansri book"),
]

seed_courses = [
    ("DB101", "Database Fundamentals"),
    ("WEB101", "Web Application Development"),
    ("PY101", "Python Programming"),
]

with sqlite3.connect(DATABASE) as connection:
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executemany(
        "INSERT OR IGNORE INTO tbl_std (std_id, std_name) VALUES (?, ?)",
        seed_students,
    )
    connection.executemany(
        "INSERT OR IGNORE INTO tbl_course (course_code, course_name) VALUES (?, ?)",
        seed_courses,
    )
    connection.commit()

print(f"สร้างฐานข้อมูลแล้ว: {DATABASE}")
