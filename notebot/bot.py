import logging
import sys
import json
import functools

import telegram as t
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    Filters,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from dbcontroller import DBController

with open("config.json", "r") as f:
    config = json.load(f)


class Action:
    defaults = {
        "create": ["text", "name"],
        "read": ["rowid"],
        "update": ["text", "name", "rowid"],
        "delete": ["rowid"],
    }

    def __init__(self, command):
        self.command = command
        self.name = command[1:]
        self.required_fields = Action.defaults[self.command]
        self.request = str()
        self.data = dict()


# Conversation state constants
SELECTING_ACTION, COLLECTING_DATA, PROCESSING_ACTION, EXECUTED_ACTION = range(4)

# Command buttons definition
commands = [InlineKeyboardButton(c, callback_data=c) for c in Action.defaults.keys()]

keyboard = [[commands[0], commands[1]], [commands[2], commands[3]]]
reply_markup = InlineKeyboardMarkup(keyboard)


def restricted(func):
    "Restriction decorator for admin-only access"

    @functools.wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != config["bot"]["admin"]:
            logging.warning(f"Unauthorized: access denied for {user_id}")
            return
        return func(update, context, *args, **kwargs)

    return wrapped


@restricted
def start(update, context):
    "/start command"
    context.user_data["database"] = DBController(config["database"]["path"])
    bot_info = str(context.bot.get_me())
    message = f"Select an action"
    update.message.reply_text(message, reply_markup=reply_markup)
    return SELECTING_ACTION


def action(update, context):
    "Inline command button"
    query = update.callback_query

    action = Action(query.data)

    for field in action.required_fields:
        message = f"Selected option: {query.data}\nEnter {field.upper()} value"
        query.edit_message_text(text=message)
        return COLLECTING_DATA


def cancel(update, context):
    pass


## MAIN ###


def main():
    logging.basicConfig(format=config["log"]["format"], level=config["log"]["level"])

    up = Updater(token=config["bot"]["token"], use_context=True)
    dp = up.dispatcher

    start_handler = CommandHandler("start", start)
    button_handler = CallbackQueryHandler(create_action)
    collecting_data_handler = MessageHandler(Filters.text, create_action)

    main_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            SELECTING_ACTION: [button_handler],
            COLLECTING_DATA: [collecting_data_handler],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(main_handler)

    up.start_polling()


if __name__ == "__main__":
    main()
