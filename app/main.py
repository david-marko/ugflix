from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, redirect, jsonify, session
import requests, uuid
from base64 import b64encode
import mysql.connector

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

pub_key = os.getenv('flwv_pubkey')
sec_key = os.getenv('flwv_seckey')
crypto_key = os.getenv('privacygate')

host = os.getenv('host')
bot_name = os.getenv('bot_name')

app = Flask(__name__)
app.secret_key = 'secret_key'
flutterwave_url = "https://api.flutterwave.com/v3/payments"

@app.route('/')
def hello():
    return 'Movies'

@app.route('/payment/<string:page>')
def payment(page):
    user_id = request.args.get("user_id")
    f_name = request.args.get("first_name")
    username = request.args.get("username")
    if page == 'crypto':
        charge_url = "https://api.privacygate.io/charges"
        r = requests.post(charge_url, headers={
                            "Content-Type": "application/json",
                            "X-CC-Api-Key": crypto_key,
                            "X-CC-Version": "2018-03-22"
                          },
                          json={
            "name": "UGFlix",
            "description": "Source for Translated and Non-translated movies",
            "local_price": {
                "amount": "5.00",
                "currency": "USD"
            },
            "pricing_type": "fixed_price",
            "metadata": {
                "customer_id": user_id,
                "username": f_name+" - "+username
            },
            "redirect_url": "https://ugflix.vercel.app/completed/page",
            "cancel_url": "https://charge/canceled/page"
        })
        # print(r.content)
        if r.status_code == 200:
            link = r.json()['data']['hosted_url']
            return jsonify({'status':'success', 'link': link})
        else:
            return "Error"
    elif page == 'momo':
        txref = uuid.uuid4().hex
        r = requests.post(flutterwave_url, headers = {
            "Authorization": "Bearer "+sec_key  
        }, json={"tx_ref": txref,
            "amount": "1500",
            "currency": "UGX",
            "redirect_url": "https://t.me/@"+bot_name,
            "meta": {
                "consumer_id": int(user_id),
                "username": username
            },
            "payment_options":"mobilemoneyuganda",
            "email": "ugflix@gmail.com",
            "customer": {
                "email": "ugflix@gmail.com",
                "name": f_name,
                "phonenumber": "07812345678"
            },
            "customizations": {
                "title": "UGFlix Payments",
                "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
            }}
        )
        # print(r.content)
        if r.status_code == 200:
            link = r.json()['data']['link']
            return jsonify({'status':'success', 'link': link})
        else:
            return "Error"
    elif page == 'card':
        txref = uuid.uuid4().hex
        r = requests.post(flutterwave_url, headers = {
            "Authorization": "Bearer "+sec_key  
        }, json={"tx_ref": txref,
            "amount": "5",
            "currency": "USD",
            "redirect_url": "https://t.me/@"+bot_name,
            "meta": {
                "consumer_id": int(user_id),
                "username": username
            },
            "email": "ugflix@gmail.com",
            "customer": {
                "email": "ugflix@gmail.com",
                "name": f_name,
                "phonenumber": "07812345678"
            },
            "customizations": {
                "title": "UGFlix Payments",
                "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
            }}
        )
        # print(r.content)
        if r.status_code == 200:
            link = r.json()['data']['link']
            return jsonify({'status':'success', 'link': link})
        else:
            return "Error"

@app.route('/callback/<string:page>', methods=['GET', 'POST'])
def callbacks(page):
    if page == 'crypto':
        if request.method == 'POST':
            data = request.form['event']
            customer_id = data['data']['metadata']['customer_id']
            event_type = data['type']
            if event_type == "charge:confirmed":
                # Include to database
                check = db("SELECT * FROM `subscription` WHERE `user_id` = "+str(customer_id)+";")
                if check:
                    db("UPDATE `subscription` SET `Status`=0 WHERE `user_id` = "+str(customer_id)+";",'update')
                    db("INSERT INTO `subscription`(`id`, `user_id`, `Plan`, `Created`, `Next_billing`) VALUES (NULL,"+str(customer_id)+",'Free',CURRENT_TIMESTAMP(),date_add(CURRENT_TIMESTAMP(),interval 1 month));", 'insert')
            return "Okay", 200
    elif page == 'flutterwave':
        if request.method == 'POST':
            data = request.form['data']
            txref = data['tx_ref']
            status = data['status']
            customer_id = data['meta']['customer_id']
            username = data['meta']['username']
            if status == "successful":
                # Add monthly billing
                check = db("SELECT * FROM `subscription` WHERE `user_id` = "+str(customer_id)+";")
                if check:
                    db("UPDATE `subscription` SET `Status`=0 WHERE `user_id` = "+str(customer_id)+";",'update')
                    db("INSERT INTO `subscription`(`id`, `user_id`, `Plan`, `Created`, `Next_billing`) VALUES (NULL,"+str(customer_id)+",'Free',CURRENT_TIMESTAMP(),date_add(CURRENT_TIMESTAMP(),interval 1 month));", 'insert')
            return "Okay", 200
    elif page == 'paypal':
        pass

# @app.route('/verify/<string:page>', methods=['GET', 'POST'])
# def verify(page):
#     # Incase of redirect, verify tx_ref and update the database
#     if page == 'flutterwave':
#         pass
#     elif page == 'crypto':
#         pass

@app.route('/admin/<page>', methods=['GET', 'POST'])
def admin(page):
    session_key = session['session_key']
    if session_key and page != 'login':
        if page == 'upload':
            pass
        elif page == 'list':
            pass
        elif page == 'logout':
            pass
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'nwaya' and password == 'Play123@cut':
            session['session_key'] = b64encode('authenticated')
            return redirect('/admin/list')
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)