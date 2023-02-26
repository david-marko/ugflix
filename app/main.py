from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, redirect, jsonify, session
import requests, uuid

load_dotenv()
pub_key = os.getenv('flwv_pubkey')
sec_key = os.getenv('flwv_seckey')
crypto_key = os.getenv('privacygate')

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
            "name": "The Sovereign Individual",
            "description": "Mastering the Transition to the Information Age",
            "local_price": {
                "amount": "5.00",
                "currency": "USD"
            },
            "pricing_type": "fixed_price",
            "metadata": {
                "customer_id": "id_1005",
                "username": "Satoshi Nakamoto"
            },
            "redirect_url": "https://charge/completed/page",
            "cancel_url": "https://charge/canceled/page"
        })
        print(r.content)
        if r.status_code == 200:
            link = r.json()['data']['hosted_url']
            return redirect(link)
        else:
            return "Error"
    elif page == 'flutterwave':
        txref = uuid.uuid4().hex
        r = requests.post(flutterwave_url, headers = {
            "Authorization": "Bearer "+sec_key  
        }, json={"tx_ref": txref,
            "amount": "1000",
            "currency": "KES",
            "redirect_url": "https://webhook.site/6142fabf-75ff-4b37-9249-9f0e5310692f",
            "meta": {
                "consumer_id": 23,
                "username": "92a3-912ba-1192a"
            },
            "email": "ugflix@gmail.com",
            "customer": {
                "email": "ugflix@gmail.com",
                "name": "Dave",
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
            return redirect(link)
        else:
            return "Error"
    elif page == 'paypal':
        pass

@app.route('/callback/<string:page>', methods=['GET', 'POST'])
def callbacks(page):
    if page == 'crypto':
        if request.method == 'POST':
            data = request.form['event']
            customer_id = data['data']['metadata']['customer_id']
            event_type = data['type']
            if event_type == "charge:confirmed":
                # Include to database
                pass
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
                pass
            return "Okay", 200
    elif page == 'paypal':
        pass

@app.route('/verify/<string:page>', methods=['GET', 'POST'])
def verify(page):
    # Incase of redirect, verify tx_ref and update the database
    if page == 'flutterwave':
        pass
    elif page == 'crypto':
        pass

@app.route('/admin/<page>', methods=['GET', 'POST'])
def admin(page):
    session_key = session['session_key']
    if session_key:
        if page == 'login':
            pass
        elif page == 'upload':
            pass
        elif page == 'list':
            pass
    else:
        pass

if __name__ == '__main__':
    app.run(debug=True)