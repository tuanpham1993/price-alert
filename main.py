from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv
from deposit.deposit import calc_deposit
from trade.margin import calc_position
from alert.price import alert_price
import spot.market as spot_market
import os
import re

load_dotenv()
state = 0
symbol = ''
symbols = ['CAKEBTC', 'CAKEBUSD']

alert_price()

def main():
        updater = Updater(os.environ['TELEGRAM_TOKEN'])
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("deposit", deposit))
        dispatcher.add_handler(CommandHandler("position", position))
        dispatcher.add_handler(CommandHandler("prices", prices))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))

        dispatcher.add_handler(CallbackQueryHandler(button))

        updater.start_polling()

def message(update:Update, context: CallbackContext):
    global state

    if state == 1:
        text = update.message.text
        pos = calc_position(int(text), symbol)
        update.message.reply_text(pos)

        state = 0


def deposit(update: Update, context: CallbackContext):
    budget = calc_deposit()
    update.message.reply_text(f'Deposit budget {"{:,.0f}".format(budget)}đ')


def prices(update: Update, context: CallbackContext):
    result = []

    for symbol in symbols:
        result.append({
            'name': symbol,
            'price': spot_market.get_current_price(symbol)
        })

    update.message.reply_text(result)

def position(update: Update, context: CallbackContext):
    keyboard = [[
        InlineKeyboardButton("CAKEBTC", callback_data='position_CAKEBTC'),
        InlineKeyboardButton("CAKEBUSD", callback_data='position_CAKEBUSD'),
    ]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Chose symbol:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    global state
    global symbol

    query = update.callback_query
    query.answer()

    if re.search('position_', query.data):
        symbol = re.findall('position_(.*)', query.data)[0]
        query.edit_message_text(text="Enter num of orders")
        state = 1 # wait for num of orders

if __name__ == "__main__":
    main()