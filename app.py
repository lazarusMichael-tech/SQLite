from pathlib import Path
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "local-student-app"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@app.route("/")
def index():
    with get_db() as connection:
        students = connection.execute(
            """
            SELECT s.std_id, s.std_name,
                   COUNT(e.enrollment_id) AS course_count
            FROM tbl_std AS s
            LEFT JOIN tbl_enrollment AS e ON e.std_id = s.std_id
            GROUP BY s.std_id, s.std_name
            ORDER BY s.std_id
            """
        ).fetchall()
        courses = connection.execute(
            """
            SELECT c.course_code, c.course_name, COUNT(e.enrollment_id) AS student_count
            FROM tbl_course AS c
            LEFT JOIN tbl_enrollment AS e ON e.course_id = c.course_id
            GROUP BY c.course_id, c.course_code, c.course_name
            ORDER BY c.course_code
            """
        ).fetchall()
    return render_template("index.html", students=students, courses=courses)


@app.route("/students/new", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        std_id = request.form.get("std_id", "").strip()
        std_name = request.form.get("std_name", "").strip()
        if not std_id.isdigit() or not std_name:
            flash("กรุณากรอกรหัสนักเรียนเป็นตัวเลขและชื่อให้ครบถ้วน", "error")
            return render_template("add_student.html")

        try:
            with get_db() as connection:
                connection.execute(
                    "INSERT INTO tbl_std (std_id, std_name) VALUES (?, ?)",
                    (int(std_id), std_name),
                )
                connection.commit()
        except sqlite3.IntegrityError:
            flash("รหัสนักเรียนนี้มีอยู่แล้ว", "error")
            return render_template("add_student.html")

        flash("เพิ่มข้อมูลนักเรียนเรียบร้อยแล้ว", "success")
        return redirect(url_for("index"))

    return render_template("add_student.html")


@app.route("/courses/new", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        course_code = request.form.get("course_code", "").strip().upper()
        course_name = request.form.get("course_name", "").strip()
        if not course_code or not course_name:
            flash("กรุณากรอกรหัสวิชาและชื่อวิชาให้ครบถ้วน", "error")
            return render_template("add_course.html")

        try:
            with get_db() as connection:
                connection.execute(
                    "INSERT INTO tbl_course (course_code, course_name) VALUES (?, ?)",
                    (course_code, course_name),
                )
                connection.commit()
        except sqlite3.IntegrityError:
            flash("รหัสวิชานี้มีอยู่แล้ว", "error")
            return render_template("add_course.html")

        flash("เพิ่มรายวิชาเรียบร้อยแล้ว", "success")
        return redirect(url_for("index"))

    return render_template("add_course.html")


@app.route("/enrollments/new", methods=["GET", "POST"])
def add_enrollment():
    with get_db() as connection:
        students = connection.execute(
            "SELECT std_id, std_name FROM tbl_std ORDER BY std_id"
        ).fetchall()
        courses = connection.execute(
            "SELECT course_id, course_code, course_name FROM tbl_course ORDER BY course_code"
        ).fetchall()

        if request.method == "POST":
            try:
                connection.execute(
                    "INSERT INTO tbl_enrollment (std_id, course_id) VALUES (?, ?)",
                    (int(request.form["std_id"]), int(request.form["course_id"])),
                )
                connection.commit()
            except (KeyError, ValueError, sqlite3.IntegrityError):
                flash("ข้อมูลการลงทะเบียนไม่ถูกต้องหรือมีรายการนี้แล้ว", "error")
                return render_template(
                    "add_enrollment.html", students=students, courses=courses
                )

            flash("บันทึกการลงทะเบียนเรียบร้อยแล้ว", "success")
            return redirect(url_for("index"))

    return render_template("add_enrollment.html", students=students, courses=courses)


if __name__ == "__main__":
    app.run(debug=True)
