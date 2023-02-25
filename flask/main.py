from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Movies'

@app.route('/payment/<string:page>')
def payment(page):
    user_id = request.args.get("user_id")
    f_name = request.args.get("first_name")
    username = request.args.get("username")
    if page == 'crypto':
        pass
    elif page == 'flutterwave':
        pass
    elif page == 'paypal':
        pass

@app.route('/callback/<string:page>', methods=['GET', 'POST'])
def callbacks(page):
    if page == 'crypto':
        pass
    elif page == 'flutterwave':
        pass
    elif page == 'paypal':
        pass

if __name__ == '__main__':
    app.run(debug=True)