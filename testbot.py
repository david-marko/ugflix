import telebot
from telebot import types
from functions import *
import requests
import re

bot = telebot.TeleBot(bot_token)
bot_name = "UGFlix"
host = "https://ugflix.vercel.app"

admin = "someboddy"
bot = telebot.TeleBot('6162698092:AAHCqdH2_3HBhBaF_cfC-t_GA_KP5QmwSDw')

# Define the initial state
state = {}

# Define the commands that the user can use
commands = {
    'start': 'Welcome to my bot! Please choose an option:', # Check Subscription
    'renew': 'You chose option 1. What would you like to do next?', 
    'home': 'You chose option 2. What would you like to do next?',
    'search': 'You chose option 2. What would you like to do next?',
    'continue': 'You chose option 2. What would you like to do next?',
    'series': 'You chose option 2. What would you like to do next?',
    'movies': 'You chose option 2. What would you like to do next?',
    'help': 'For support, please contact @admin',
    'back': 'Going back to the previous menu.'
}

# Define the message handlers
@bot.message_handler(commands=['start'])
def start_command(message):
    state[message.chat.id] = 'start'
    if not check_user(message):
        user_id = message.from_user.id
        f_name = message.from_user.first_name
        username = message.from_user.username
        last_id = db("INSERT INTO `users` (`id`, `user_id`, `first_name`, `username`, `Created`, `Comment`, `Status`) VALUES (NULL, '" +
                     str(user_id)+"', '"+f_name+"', '"+username+"', current_timestamp(), '', '1');", 'insert')
        # Add free trial
        db("INSERT INTO `subscription`(`id`, `user_id`, `Plan`, `Created`, `Next_billing`) VALUES (NULL," +
           str(user_id)+",'Free',CURRENT_TIMESTAMP(),date_add(CURRENT_TIMESTAMP(),interval 5 day));", 'insert')
    if check_bot(message):
        bot.reply_to(message, "We are sorry, this account is not allowed")
    else:
        check_sub = check_subscriptions(message)
        if check_sub[0] == True:
            if check_sub[2] == 'Free':
                bot.reply_to(message, "Your %s trial plan has been activated for %s days" % (
                    check_sub[2], str(check_sub[1])))
            else:
                bot.reply_to(message, "Your %s plan is active and expires in %s days" % (
                    check_sub[2], str(check_sub[1])))
            state[message.chat.id] = 'home'
            bot.reply_to(message, "Welcome to your one source of entertainment for Translated and Non-translated Movies / Series", 
                         reply_markup=create_keyboard(['Search', 'Latest', 'Popular', 'Continue', 'Movies', 'Series', 'Help']))
        else:
            state[message.chat.id] = 'renew'
            bot.reply_to(message, "Renew Your Subscription", reply_markup=create_keyboard(['Get Access', 'Back']))

@bot.message_handler(func=lambda message: get_state(message.chat.id) == 'home')
def option1_command(message):
    if message.text == 'Search':
        state[message.chat.id] = 'search'
        bot.reply_to(message, "Find Movie or Series by replying with the name or title", reply_markup=create_keyboard(['Back']))
    elif message.text == 'Back':
        state[message.chat.id] = 'start'
        bot.reply_to(message, commands['start'], reply_markup=create_keyboard(['Option 1', 'Option 2']))
    elif message.text == 'Back':
        state[message.chat.id] = 'start'
        bot.reply_to(message, commands['start'], reply_markup=create_keyboard(['Option 1', 'Option 2']))


# Search navigation


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
        bot.send_message(message.chat.id, "", reply_markup=keyboard)
        bot.send_message(
            message.chat.id, "🔒 Make Payment with your preferred currency")
        # bot.send_message(message.chat.id, link)
        bot.send_message(
            message.chat.id, "Select /start when done with payment")
    else:
        bot.send_message(
            message.chat.id, "There was an error. Please contact admin @"+admin)

@bot.message_handler(commands=['back'])
def back_command(message):
    state[message.chat.id] = 'start'
    bot.reply_to(message, commands['start'], reply_markup=create_keyboard(['Option 1', 'Option 2']))

# Define the helper functions
def create_keyboard(options):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(option) for option in options]
    keyboard.add(*buttons)
    return keyboard

def get_state(chat_id):
    return state.get(chat_id, 'start')

# Start the bot
bot.polling()
