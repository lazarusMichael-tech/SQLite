PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS tbl_std (
    std_id INTEGER PRIMARY KEY,
    std_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tbl_course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT NOT NULL UNIQUE,
    course_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tbl_enrollment (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    std_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (std_id, course_id),
    FOREIGN KEY (std_id) REFERENCES tbl_std (std_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES tbl_course (course_id) ON DELETE CASCADE
);
