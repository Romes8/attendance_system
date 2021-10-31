from django.db import connection
from datetime import datetime

def get_role(username, password):
    cur = connection.cursor()
    try:
        func = "SELECT checkLogin(%s,SHA1(%s))"
        cur.execute(func, (username, password))
        role = cur.fetchone()[0]
        return role
    finally:
        cur.close()


def get_userID(role, username):
    cur = connection.cursor()
    try:
        if role == 'student':
            cur.execute("SELECT getStudentID(%s)", username)
        elif role == 'teacher':
            cur.execute("SELECT getTeacherID(%s", username)
        user_id = int(cur.fetchone()[0])
        return user_id
    finally:
        cur.close()


def get_courses(username):
    cur = connection.cursor()
    try:
        data = []
        print("calling")
        cur.callproc("teacher_courses", [username, ])
        print("executed")
        for record in cur.fetchall():
            print(record)
            data.append(
                {
                    "class": record[0],
                    "subject": record[1]
                }
            )
            print(data)
        return data

    finally:
        cur.close()

def history(student_id, sort):
    cur = connection.cursor()
    try:
        data = []
        cur.callproc("history", [student_id, sort])
        for row in cur.fetchall():
            data.append({'date': row[0].strftime("%Y-%m-%d"), 'subject': row[1], 'status': row[2]})
        return data
    finally:
        cur.close()
