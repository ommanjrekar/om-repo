import psycopg2


conn = psycopg2.connect(host="localhost", port="5432", database="postgres", user="postgres", password="postgres")#setting the connection for db
db_curs = conn.cursor()#database cursor for databse operations
#command1 = '''DROP TABLE EMPLOYEE'''
#db_curs.execute(command1)
#conn.commit()
command = '''CREATE TABLE EMPLOYEE(
   ID INTEGER PRIMARY KEY,
   NAME CHAR(20) NOT NULL,
   DOJ CHAR(20) NOT NULL,
   EDU CHAR(20) NOT NULL,
   LOC CHAR(20) NOT NULL
)'''   #command to create table
db_curs.execute(command) #to execute the command
with open('emp.csv', 'r') as f: #reading a csv file which is to copy to db
    next(f) #ignoring the headers
    db_curs.copy_from(f, 'EMPLOYEE', sep=',') #copy csv to db table EMPLOYEE
conn.commit() #commit the transaction 
print("Table created successfully........")
conn.close() #closing the connection
