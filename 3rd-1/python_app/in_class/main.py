import sqlite3


class hey:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    def create_student_table(self):
        self.cur.execute(
            "CREATE TABLE students(id integer primary key , name text, gender text)"
        )
        self.con.commit()

    def insert_student(self, name, gender):
        self.cur.execute(
            "insert into students(name, gender) values(?, ?)", (name, gender)
        )
        self.con.commit()

    def list_student(self):
        result = self.cur.execute("select * from students")
        students = result.fetchall()
        for student in students:
            print(student)


myc = hey("myInfo.db")
# myc.create_student_table()
myc.insert_student("Ray", "M")
myc.list_student()
