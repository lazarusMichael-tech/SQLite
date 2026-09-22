# Michael Student Hub

เว็บแอปพลิเคชัน Local สำหรับจัดการข้อมูลนักเรียนจากฐานข้อมูลเดิมของงานที่ 8 โดยใช้ Python Flask และ SQLite

## ตารางในระบบ

- `tbl_std` ข้อมูลนักเรียนเดิมจากฐานข้อมูล `michael`
- `tbl_course` ข้อมูลรายวิชา
- `tbl_enrollment` ความสัมพันธ์ระหว่างนักเรียนกับรายวิชา

ข้อมูลตัวอย่างนักเรียนจากงานที่ 8 ถูกใส่ไว้ในไฟล์ SQLite แล้ว และจะไม่หายเมื่อปิดแล้วเปิดระบบใหม่

## วิธีรันบน Windows

1. เปิด PowerShell ในโฟลเดอร์นี้
2. สร้าง virtual environment (แนะนำ):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. ติดตั้ง Flask:

   ```powershell
   pip install -r requirements.txt
   ```

4. สร้างหรือเติมข้อมูลเริ่มต้น:

   ```powershell
   python init_db.py
   ```

5. เปิดเว็บ:

   ```powershell
   python app.py
   ```

6. เปิดเบราว์เซอร์ที่ <http://127.0.0.1:5000>

## ไฟล์สำคัญ

- `app.py` โค้ดเว็บ Flask และคำสั่ง SELECT/INSERT
- `students.db` ฐานข้อมูล SQLite ที่ใช้งานจริง
- `schema.sql` โครงสร้างตาราง
- `init_db.py` สร้างตารางและข้อมูลตัวอย่าง
