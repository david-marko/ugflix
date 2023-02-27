import telebot
from telebot import types
from functions import *
import requests
import re

bot = telebot.TeleBot(bot_token)
bot_name = "UGFlix"
host = "https://ugflix.vercel.app"

admin = "someboddy"


@bot.message_handler(commands=['start', 'hello', "Back_Home"])
def send_welcome(message):
    if not check_user(message):
        user_id = message.from_user.id
        f_name = message.from_user.first_name
        username = message.from_user.username
        last_id = db("INSERT INTO `users` (`id`, `user_id`, `first_name`, `username`, `Created`, `Comment`, `Status`) VALUES (NULL, '" +
                     str(user_id)+"', '"+f_name+"', '"+username+"', current_timestamp(), '', '1');", 'insert')
        # Add free trial
        db("INSERT INTO `subscription`(`id`, `user_id`, `Plan`, `Created`, `Next_billing`) VALUES (NULL," +
           str(user_id)+",'Free',CURRENT_TIMESTAMP(),date_add(CURRENT_TIMESTAMP(),interval 5 day));", 'insert')
    # if bot, dont allow
    if check_bot(message):
        bot.reply_to(message, "We are sorry, this account is not allowed")
    else:
        # Check subscription
        check_sub = check_subscriptions(message)
        if check_sub[0] == True:
            bot.reply_to(message, "Hello %s, Welcome to %s " %
                         (message.from_user.first_name, bot_name))
            if check_sub[2] == 'Free':
                bot.reply_to(message, "Your %s trial plan has been activated for %s days" % (
                    check_sub[2], str(check_sub[1])))
            else:
                bot.reply_to(message, "Your %s plan is active and expires in %s days" % (
                    check_sub[2], str(check_sub[1])))
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            itembtn1 = types.KeyboardButton('/continue')
            itembtn5 = types.KeyboardButton('/search')
            itembtn2 = types.KeyboardButton('/series')
            itembtn3 = types.KeyboardButton('/movies')
            itembtn4 = types.KeyboardButton('/help')
            markup.add(itembtn5, itembtn1, itembtn2, itembtn3, itembtn4)
            bot.send_message(
                message.chat.id, "Select Category of Translated and Non-Translated Movies", reply_markup=markup)
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=1)
            # Create a custom keyboard button
            button = types.KeyboardButton('/renew')
            # Add the button to the keyboard layout
            keyboard.add(button)
            bot.reply_to(message, "Hello %s, Your %s Plan expired %s days ago" % (
                message.from_user.first_name, check_sub[2], str(check_sub[1])), reply_markup=keyboard)


@bot.message_handler(commands=['renew'])
def renew_options(message, res=False):
    print("Renewing")
    markup = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
    itembtn1 = types.KeyboardButton('/MoMo')
    itembtn2 = types.KeyboardButton('/Card')
    itembtn4 = types.KeyboardButton('/Crypto')
    markup.add(itembtn1, itembtn2, itembtn4)
    bot.send_message(
        message.chat.id, "Choose Option to pay Monthly Premium access:", reply_markup=markup)
    pay_details = """
    - Use MoMo for Airtel or MTN (12,000 UGX)
    - Use Card for Visa or Mastercard (5 USD)
    - Use Crypto for BTC, LTC, ETH and more (5 USD)
    """
    bot.send_message(message.chat.id, pay_details, reply_markup=markup)
    # bot.send_message(message.chat.id, "Choose Option to pay $5 Monthly Premium access:")


@bot.message_handler(commands=['MoMo'])
def momo_renew(message, res=False):
    print("Initiating Mobile Money")
    user_id = message.from_user.id
    f_name = message.from_user.first_name
    username = message.from_user.username
    r = requests.get(host+"/payment/momo", params={
        "user_id": user_id,
        "first_name": f_name,
        "username": username
    })
    # print(r.content)
    if r.status_code == 200:
        link = r.json()['link']
        bot.send_message(
            message.chat.id, "Click the link below to securely complete the payment of 12,000 ugx using mobile money (MTN or Airtel)")
        bot.send_message(
            message.chat.id, "Chose Mobile Money as Payment Method")
        bot.send_message(
            message.chat.id, "🔒 This transaction is secured by Flutterwave")
        bot.send_message(message.chat.id, link)
        bot.send_message(
            message.chat.id, "Select /start when done with payment")
    else:
        bot.send_message(
            message.chat.id, "There was an error. Please contact admin @"+admin)


@bot.message_handler(commands=['Card'])
def momo_renew(message, res=False):
    print("Initiating Card")
    user_id = message.from_user.id
    f_name = message.from_user.first_name
    username = message.from_user.username
    r = requests.get(host+"/payment/card", params={
        "user_id": user_id,
        "first_name": f_name,
        "username": username
    })
    # print(r.content)
    if r.status_code == 200:
        link = r.json()['link']
        bot.send_message(
            message.chat.id, "Click the link below to securely complete the payment of 5 USD using Visa or MasterCard")
        bot.send_message(message.chat.id, "Chose Card as Payment Method")
        bot.send_message(
            message.chat.id, "🔒 This transaction is secured by Flutterwave")
        bot.send_message(message.chat.id, link)
        bot.send_message(
            message.chat.id, "Select /start when done with payment")
    else:
        bot.send_message(
            message.chat.id, "There was an error. Please contact admin @"+admin)


@bot.message_handler(commands=['Crypto'])
def momo_renew(message, res=False):
    print("Initiating Crypto")
    user_id = message.from_user.id
    f_name = message.from_user.first_name
    username = message.from_user.username
    r = requests.get(host+"/payment/crypto", params={
        "user_id": user_id,
        "first_name": f_name,
        "username": username
    })
    # print(r.content)
    if r.status_code == 200:
        link = r.json()['link']
        bot.send_message(
            message.chat.id, "Click the link below to securely complete the payment of 5 USD using Crypto")
        bot.send_message(
            message.chat.id, "Choose your preffered Crypto Currency")
        bot.send_message(message.chat.id, link)
        bot.send_message(
            message.chat.id, "Select /start when done with payment")
    else:
        bot.send_message(
            message.chat.id, "There was an error. Please contact admin @"+admin)


@bot.message_handler(commands=["continue"])  # user command
def continue_watching(m, res=False):
    bot.send_message(m.chat.id, "Help: For any help, please contact @"+admin)

@bot.message_handler(commands=["series", "back_to_series"])  # user command
def series_cat(m, res=False):
    markup = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
    itembtn1 = types.KeyboardButton('/Translated_Series')
    itembtn2 = types.KeyboardButton('/English_Series')
    itembtn3 = types.KeyboardButton('/Back_Home')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(m.chat.id, "Select Series Category", reply_markup=markup)

@bot.message_handler(commands=["Translated_Series"])  # user command
def translated_series(m, res=False):
    # markup = types.ReplyKeyboardMarkup(
    #     row_width=2, resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
    # itembtn1 = types.InlineKeyboardButton('/Action', callback_data='/Translated_Category Action')
    # itembtn2 = types.InlineKeyboardButton('/Adventure')
    # itembtn3 = types.InlineKeyboardButton('/Comedy')
    # itembtn4 = types.InlineKeyboardButton('/back_to_series')
    # markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    markup = telebot.util.quick_markup(
        {'text': 'Press me', 'callback_data': 'press'},
        {'text': 'Press me too', 'callback_data': 'press_too'}
    )
    bot.send_message(m.chat.id, "Select the Genre of translated series", reply_markup=markup)

@bot.message_handler(commands=["movies"])  # user command
def start(m, res=False):
    bot.send_message(m.chat.id, "Help: For any help, please contact @"+admin)

@bot.message_handler(commands=["continue"])  # user command
def start(m, res=False):
    bot.send_message(m.chat.id, "Help: For any help, please contact @"+admin)

@bot.message_handler(commands=['Translated_Category'])
def searcher(message, res=False):
    command = telebot.util.extract_arguments(message.text)
    print(command)


@bot.message_handler(commands=['search'])
def after_text(message):
    print(message.text)
    if message.text == '/search':
        msg = bot.send_message(message.chat.id, 'Enter Movie Name or Title')
        bot.register_next_step_handler(msg, after_text_2)

def after_text_2(message):
    print('the phone number entered by the user at the "sms" step:', message.text)


@bot.message_handler(commands=["Help"])  # user command
def start(m, res=False):
    bot.send_message(m.chat.id, "Help: For any help, please contact @"+admin)


@bot.message_handler(commands=['forward'], content_types=['text', 'video', 'photo'])
def forward_video(message):
    # Forward a video from your channel to the user
    video_id = '3'
    # bot.for
    # bot.kick_chat_member(chat_id='@meandiug', user_id=1609763046)
    bot.forward_message(chat_id=message.chat.id,
                        from_chat_id='@meandiug', message_id=video_id)


bot.infinity_polling()
