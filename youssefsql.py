import sqlite3 as yomna

def create_table(): #creates a table (if it is not already there)
    con = yomna.connect("data.db")
    curs = con.cursor()

    curs.execute("CREATE TABLE IF NOT EXISTS sdata (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, term INTEGER, gpa REAL)")

    con.commit()
    con.close()

def insert(fname, lname, term, gpa): #inserts data
    con = yomna.connect("data.db")
    curs = con.cursor()

    curs.execute("INSERT INTO sdata VALUES (NULL, ?,?,?,?)", (fname, lname, term, gpa))

    con.commit()
    con.close()

def view(): #views data
    con = yomna.connect("data.db")
    curs = con.cursor()

    curs.execute("SELECT * FROM sdata")
    data = curs.fetchall()

    con.commit()
    con.close()

    return data

def remove(id):#removes a certain row according to id
    con = yomna.connect("data.db")
    curs = con.cursor()

    curs.execute("DELETE FROM sdata WHERE id = ?", (id,))

    con.commit()
    con.close()

def search(id = '', fname = '', lname = '', term = '', gpa = ''): #searches for a certain student
    con = yomna.connect("data.db")
    curs = con.cursor()

    curs.execute("SELECT * FROM sdata WHERE id = ? OR fname = ? OR lname = ? OR term = ? OR gpa = ? ", (id,fname, lname, term, gpa))
    data = curs.fetchall()

    con.commit()
    con.close()
    return data

def clear(): #deletes all table data
    con = yomna.connect("data.db")
    curs = con.cursor()

    curs.execute("DELETE FROM sdata")

    con.commit()
    con.close()

def update(id, fname, lname, term, gpa):
    con = yomna.connect("data.db")
    curs = con.cursor()

    curs.execute("UPDATE sdata SET fname = ?, lname = ?, term = ?, gpa = ? WHERE id = ?", (fname, lname, term, gpa, id))

    con.commit()
    con.close()


############ MAIN ###########
create_table()
insert('yomna', 'omar', 9, 2.85)
insert('yofwefmna', 'oqwdmar', 329, 322.85)
insert('yomwefwefna', 'omaqdwr', 49, 2.23485)
insert('yomwqena', 'omaqwdwr', 94, 2.8534)
# remove(1)
# remove(2)

print(view())

# print(search(lname = 'omar'))