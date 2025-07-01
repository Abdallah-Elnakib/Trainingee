import mysql.connector
from mysql.connector import Error


#  "host": 'srv508.hstgr.io',
#     "user": 'u394601625_abdallah',
#     "password": 'ZA&&na158269347',
#     "database": 'u394601625_traininge'


from mysql.connector import Error
try:
        mydb = mysql.connector.connect(host='srv508.hstgr.io', user='u394601625_abdallah', passwd='ZA&&na158269347', port=3306, database='u394601625_traininge')
        my_cursor = mydb.cursor()
            
except Error as e:
    print('Error No internet connection please check your connection and try again')
    
# my_cursor.execute('ALTER TABLE tracks_name ADD name_in_database VARCHAR(100)')
# my_cursor.execute('SELECT * FROM student_information')
# result = my_cursor.fetchall()
# var0 = 0
# for i in result:
#     var0 = i[0]
# print(var0)
# my_cursor.execute('CREATE DATABASE Trainingee')

#my_cursor.execute('CREATE TABLE student_information (id VARCHAR(100) , name VARCHAR(100), degrees VARCHAR(100) , additional_degrees VARCHAR(100),  total VARCHAR(100), commintent VARCHAR(100), total_degrees VARCHAR(100))')
# my_cursor.execute('CREATE TABLE tracks_name (name VARCHAR(100))')
# my_cursor.execute('ALTER TABLE track5 ADD track_nmae VARCHAR(100)')
# mydb.commit()

# my_cursor.execute('DROP TABLE student_information')  #To delete Table

# my_cursor.execute('ALTER TABLE javascript DROP COLUMN end')

# my_cursor.execute('SHOW TABLES') #to show all table
# result = my_cursor.fetchall()
# print(result)
# for i in result:
#     if i != result[0]:
#         sql = f'SELECT * FROM {i[0]} WHERE name LIKE %s OR id = %s'
#         data_base = ('%' + entry_name + '%', entry_name)
#         my_cursor.execute(sql, data_base)
#         result = my_cursor.fetchone()

# DELETE FROM table_name WHERE condition

# my_cursor.execute('ALTER TABLE Node_Js RENAME track4')

# my_cursor.execute('SHOW TABLES')
# result = my_cursor.fetchall()
# print(result)


# sql = 'UPDATE track5 SET track_name = %s where id = %s' 
# val = ("test",'2')
# my_cursor.execute(sql, val)
# mydb.commit()


# sql = 'INSERT INTO tracks_name (name, name_in_database) VALUES(%s, %s)'
# val = ('track5', 'test')
# my_cursor.execute(sql, val)
# mydb.commit()


# sql = 'SELECT TOP 5 FROM student_information'

# my_cursor.execute('SELECT TOP 5 FROM student_information WHERE total')
# result = my_cursor.fetchall()
# print(result)


 
# my_cursor.execute('DELETE FROM javascript WHERE id = 42')


# sql = f"DELETE FROM javascript WHERE id = %s"
# val =  (26,)
# my_cursor.execute(sql, val)
# mydb.commit()



# my_cursor.execute(f'SELECT * FROM tracks_name')
# result_after = my_cursor.fetchall()
# print(result_after)
# # for i in result_after:
# #        print(i)

# my_cursor.execute(f'SELECT * FROM tracks_name')
# result_after = my_cursor.fetchall()
# last_name = result_after[len(result_after) - 1][0]
# last_number = int(last_name[len(last_name) - 1]) + 1
# name_track_in_database = 'track' + str(last_number)

