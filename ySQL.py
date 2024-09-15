import mysql.connector

#connect to server
mydb = mysql.connector.connect(
    host = "localhost", 
    user = "admin", 
    passwd = "mysqltest2admin",
)
curs = mydb.cursor()

#create data base and reconnect to server
curs.execute("CREATE DATABASE IF NOT EXISTS studentsDATABASE")
mydb = mysql.connector.connect(
    host = "localhost", 
    user = "admin", 
    passwd = "mysqltest2admin",
    database = "studentsDATABASE"
)
curs = mydb.cursor()
##################################################################################################

#create table
def create_table():
    sql = "CREATE TABLE IF NOT EXISTS sdata(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), gpa FLOAT, term INT, time_enroll VARCHAR(255))"
    curs.execute(sql)
    mydb.commit()
    return

create_table()

##################################################################################################

def insert(name, email, gpa, term, time_enroll):
    sql = "INSERT INTO sdata (name, email, gpa, term, time_enroll) VALUES (%s, %s,%s,%s,%s)"
    curs.execute(sql,(name, email, gpa, term, time_enroll))
    mydb.commit()
    return

##################################################################################################

def view():
    sql = "SELECT * FROM sdata"
    curs.execute(sql)
    ans = curs.fetchall()
    return ans

##################################################################################################

def delete(id):
    sql = "DELETE FROM sdata WHERE id=%s"
    curs.execute(sql, (id,))
    mydb.commit()
    return

##################################################################################################

def get_id(name, email, gpa, term, time_enroll):
    sql = "SELECT * FROM sdata WHERE name=%s AND email=%s AND gpa=%s AND term=%s AND time_enroll=%s"
    curs.execute(sql,(name, email, gpa, term, time_enroll))
    id = curs.fetchall()[0][0]
    return id
##################################################################################################

def update (id, name, email, gpa, term, time_enroll):
    sql = "UPDATE sdata SET name=%s, email=%s, gpa=%s, term=%s, time_enroll=%s WHERE id=%s"
    curs.execute(sql,(name, email, gpa, term, time_enroll, id))
    mydb.commit()
    return

##################################################################################################

def search(name='', email='', gpa='', term='', time_enroll=''):
    sql = "SELECT * FROM sdata WHERE name LIKE %s OR email LIKE %s OR gpa LIKE %s OR term LIKE %s OR time_enroll LIKE %s"
    
    if name != '' and email != '':
        curs.execute(sql,(f'%{name}%', f'%{email}%', gpa, term, time_enroll))
    elif name != '':
        curs.execute(sql,(f'%{name}%', email, gpa, term, time_enroll))
    elif email != '':
        curs.execute(sql,(name, f'%{email}%', gpa, term, time_enroll))
    else:
        curs.execute(sql,(name, email, gpa, term, time_enroll))

    ans = curs.fetchall()
    return ans

##################################################################################################

def sort(opt):
    if opt == "By Name":
        sql = "SELECT * FROM sdata ORDER BY name"
        curs.execute(sql)
        ans = curs.fetchall()
        return ans
    
    elif opt == "By Email":
        sql = "SELECT * FROM sdata ORDER BY email"
        curs.execute(sql)
        ans = curs.fetchall()
        return ans
    
    elif opt == "By GPA":
        sql = "SELECT * FROM sdata ORDER BY gpa"
        curs.execute(sql)
        ans = curs.fetchall()
        return ans
    
    elif opt == "By Term":
        sql = "SELECT * FROM sdata ORDER BY term"
        curs.execute(sql)
        ans = curs.fetchall()
        return ans
    
    elif opt == "By Date":
        sql = "SELECT * FROM sdata ORDER BY time_enroll"
        curs.execute(sql)
        ans = curs.fetchall()
        return ans
    
