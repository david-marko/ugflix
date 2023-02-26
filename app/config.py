import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

dbhost = os.getenv('dbhost')
dbuser = os.getenv('dbuser')
dbpass = os.getenv('dbpass')
dbname = os.getenv('dbname')

bot_token = os.getenv('bot_token')

def db(sql, query='select', data=None):
    conn = mysql.connector.connect(host=dbhost,user=dbuser,port=3306, password=dbpass,database=dbname)
    cursor = conn.cursor(dictionary=True,buffered=True)
    ret = []
    # sql = conn.converter.escape(sql)
    if query == 'insert':
        cursor.execute(sql,data)
    else:
        cursor.execute(sql)
    if query == 'select':
        ret = cursor.fetchone()
    elif query == 'many':
        ret = cursor.fetchall()
    elif query == 'insert':
        ret = cursor.lastrowid
        conn.commit()
    elif query == 'update':
        conn.commit()
        ret = True
    cursor.close()
    return ret