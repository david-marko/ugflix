import telebot
from telebot import types
from functions import *

bot = telebot.TeleBot(bot_token)
bot_name = "UGFlix"

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    print("Start")
    if not check_user(message):
        user_id = message.from_user.id
        f_name = message.from_user.first_name
        username = message.from_user.username
        last_id = db("INSERT INTO `users` (`id`, `user_id`, `first_name`, `username`, `Created`, `Comment`, `Status`) VALUES (NULL, '"+str(user_id)+"', '"+f_name+"', '"+username+"', current_timestamp(), '', '1');", 'insert')
        # Add free trial
        db("INSERT INTO `subscription`(`id`, `user_id`, `Plan`, `Created`, `Next_billing`) VALUES (NULL,"+str(user_id)+",'Free',CURRENT_TIMESTAMP(),date_add(CURRENT_TIMESTAMP(),interval 5 day));", 'insert')
    # if bot, dont allow
    if check_bot(message):
        bot.reply_to(message, "We are sorry, this account is not allowed")
    else:
        # Check subscription
        check_sub = check_subscriptions(message)
        if check_sub[0] == True:
            bot.reply_to(message, "Hello %s, Welcome to %s " % (message.from_user.first_name, bot_name))
            if check_sub[2] == 'Free':
                bot.reply_to(message, "Your %s trial plan has been activated for %s days" % (check_sub[2], str(check_sub[1])))
            else:
                bot.reply_to(message, "Your %s plan is active and expires in %s days" % (check_sub[2], str(check_sub[1])))
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('Popular')
            itembtn2 = types.KeyboardButton('Series')
            itembtn3 = types.KeyboardButton('Movies')
            itembtn4 = types.KeyboardButton('Documentaries')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
            bot.send_message(message.chat.id, "Select Category of Translated and Non-Translated Movies", reply_markup=markup)
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=1)
            # Create a custom keyboard button
            button = types.KeyboardButton('/renew')
            # Add the button to the keyboard layout
            keyboard.add(button)
            bot.reply_to(message, "Hello %s, Your %s Plan expired %s days ago" % (message.from_user.first_name, check_sub[2], str(check_sub[1])), reply_markup=keyboard)
    
@bot.message_handler(commands=['renew'])
def renew_options(message, res=False):
    print("Renewing")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Paypal')
    itembtn2 = types.KeyboardButton('Mobile Money')
    itembtn3 = types.KeyboardButton('Debit Card')
    itembtn4 = types.KeyboardButton('Crypto')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "Choose Option to pay $5 Monthly Premium access:", reply_markup=markup)
    # bot.send_message(message.chat.id, "Choose Option to pay $5 Monthly Premium access:")

@bot.message_handler(commands=["help"]) # user command
def start(m, res=False):
    bot.send_message(m.chat.id, "Help: ")

@bot.message_handler(commands=['forward'], content_types=['text','video','photo'])
def forward_video(message):
    # Forward a video from your channel to the user
    video_id = '3'
    # bot.for
    # bot.kick_chat_member(chat_id='@meandiug', user_id=1609763046)
    bot.forward_message(chat_id=message.chat.id, from_chat_id='@meandiug', message_id=video_id)

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     if message.text == 'Paypal':
#         bot.reply_to(message, 'You clicked Button 1!')
#     elif message.text == 'Mobile Money':
#         bot.reply_to(message, 'You clicked Button 2!')
#     elif message.text == 'Debit Card':
#         bot.reply_to(message, 'You clicked Button 3!')
#     elif message.text == 'Crypto':
#         bot.reply_to(message, 'You clicked Button 4!')

bot.infinity_polling()