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

def check_user(message):
    user_id = message.from_user.id
    username = message.from_user.username
    check = db("SELECT * FROM "+dbname+".users WHERE users.user_id = "+str(user_id)+" OR users.username = '"+username+"'")
    if check:
        return True
    else:
        return False

def check_subscriptions(message):
    user_id = message.from_user.id
    sql_days = db("SELECT DATEDIFF(subscription.Next_billing,CURRENT_DATE()) AS days, subscription.Plan FROM subscription WHERE subscription.user_id = "+str(user_id)+";")
    days = sql_days['days']
    plan = sql_days['Plan']
    if days < 0:
        return [False, days, plan]
    else:
        return [True, days, plan]

def check_bot(message):
    if message.from_user.is_bot:
        return True
    else:
        return False