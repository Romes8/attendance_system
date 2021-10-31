from django.db import connection


def get_role(username, password):
    cur = connection.cursor()
    try:
        func = "SELECT checkLogin(%s,SHA1(%s))"
        cur.execute(func, (username, password))
        result = cur.fetchone()
        return result[0]
    finally:
        cur.close()

def get_courses(username):
    cur = connection.cursor()
    try:
        data = []
        print("calling")
        cur.callproc("teacher_courses", [username,])
        print("executed")
        for row in cur.stored_results():
            for record in row.fetchall():
                print(record)
                data.append(
                    {
                        "class": record[0],
                        "subject": record[1],
                        "desc": record[2]
                    }
                )
                print(data)
        return data

    finally:
        cur.close()

def history():
cur = connection.cursor()
try:
data = []
cur.callproc("history", user_id)
for row in cur.fetchall():
data.append(row)
return data
finally:
cur.close()


