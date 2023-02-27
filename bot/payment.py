import requests
from config import bot, get_state, create_keyboard, state, host
from telebot import types


@bot.message_handler(func=lambda message: get_state(message.chat.id) == 'renew')
def renew_handler(message):
    if message.text == 'Get Access':
        state[message.chat.id] = 'pay'
        bot.reply_to(message, "Make Payment of 12,000 UGX or 5 USD to get access for one month", 
                     reply_markup=create_keyboard(['Mobile Money','Debit Card','Crypto','Back']))
    elif message.text == 'Back':
        state[message.chat.id] = 'renew'
        bot.reply_to(message, "Renew Your Subscription", reply_markup=create_keyboard(['Get Access', 'Back']))


@bot.message_handler(func=lambda message: get_state(message.chat.id) == 'pay')
def option2_command(message):
    user_id = message.from_user.id
    f_name = message.from_user.first_name
    username = message.from_user.username
    if message.text == 'Mobile Money':
        state[message.chat.id] = 'start'
        r = requests.get(host+"/payment/momo", params={
            "user_id": user_id,
            "first_name": f_name,
            "username": username
        })
    elif message.text == 'Debit Card':
        state[message.chat.id] = 'start'
        r = requests.get(host+"/payment/card", params={
            "user_id": user_id,
            "first_name": f_name,
            "username": username
        })
    elif message.text == 'Crypto':
        state[message.chat.id] = 'pay'
        r = requests.get(host+"/payment/crypto", params={
            "user_id": user_id,
            "first_name": f_name,
            "username": username
        })
    if r.status_code == 200:
        link = r.json()['link']
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            text="Make Secure Payment",
            web_app=types.WebAppInfo(url=link)
        ))
        bot.send_message(message.chat.id, "Select /start when done with payment", reply_markup=keyboard)
        bot.send_message(
            message.chat.id, "🔒 Make Payment with your preferred currency")
        # bot.send_message(message.chat.id, link)
    else:
        bot.send_message(
            message.chat.id, "There was an error. Please contact admin @admin")