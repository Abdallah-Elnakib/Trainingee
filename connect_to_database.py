from mysql.connector import Error
import mysql.connector
from dotenv import load_dotenv 
import os

def connect():
    load_dotenv()
    try:
        mydb = mysql.connector.connect(host=os.getenv('HOST'), user=os.getenv('USER'), passwd=os.getenv('PASSWORD'), port=os.getenv('PORT'), database=os.getenv('DATABASE'))
        my_cursor = mydb.cursor()
        return my_cursor
    except Error as e:
        import Verification
        Verification.connection_error()
        return
