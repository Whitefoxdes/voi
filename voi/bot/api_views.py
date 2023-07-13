import os
import json
import telebot
import requests
from telebot.types import (
    InputMediaPhoto,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from handbook.models import (
    Handbook, 
    HandbookType
)
from games.models import Games
from handbook.serializer import (
    HandbookSerializer,
    HandbookTypeSerializer
)
from voi.settings import BOT_TOKEN, BASE_DIR
from games.serializer import GamesSerializer


bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(['start'])
def start(message):
    send_msg = bot.send_message(message.chat.id, "Hello, this'is VOI bot")

@bot.message_handler(['gamesearch'])
def game_search_result(message):
    chat_id = message.chat.id
    send_msg = bot.send_message(
        chat_id,
        "Write game name, like this: Skyrim, Prey, Dishonored"
    )
    bot.register_next_step_handler(send_msg, game_search_result, user_chat_id=chat_id)

def game_search_result(
        message=None,
        url_param=None,
        user_chat_id=None
):
    if url_param:
        request_url = f"http://127.0.0.1:8000/api/v1/games/search/?{url_param}"
    else:
        request_url = f"http://127.0.0.1:8000/api/v1/games/search/?name={message.text}"

    r = requests.get(request_url)
    request_data = r.json()
    
    results = request_data.get("results")

    if not results:
        error_game_not_found_msg = bot.send_message(
            message.chat.id,
            "Game not found, write another game name"
        )
        bot.register_next_step_handler(
            error_game_not_found_msg,
            game_search_result,
            user_chat_id=message.chat.id 
        )
        return

    previous_page = request_data.get("previous")
    next_page = request_data.get("next")

    keyboard = InlineKeyboardMarkup()
    keyboard_page = InlineKeyboardMarkup()

    for game in results:
        callback_data = json.dumps(
            {
              "type": "game",
              "game_id": game.get('id')
            }
        ) 
        
        game_button = InlineKeyboardButton(
            game.get("name"),
            callback_data=callback_data
        )
        keyboard.add(game_button)

    bot.send_message(
        user_chat_id,
        "Game list",
        reply_markup=keyboard
    )

    if next_page and previous_page:
        next_page_param = next_page.split("?")[1]
        previous_page_param = previous_page.split("?")[1]

        next_page_callback_data = json.dumps(
            {
                "type": "next_page_game_search",
                "next_page": next_page_param
            }
        )
        previous_page_callback_data = json.dumps(
            {
                "type": "prev_page_game_search",
                "prev_page": previous_page_param
            }
        )

        next_page_button = InlineKeyboardButton(
            "❯",
            callback_data=next_page_callback_data
        )
        previous_page_button = InlineKeyboardButton(
            "❮",
            callback_data=previous_page_callback_data
        )

        keyboard_page.add(
            previous_page_button,
            next_page_button
        )
        bot.send_message(
            user_chat_id,
            "Select page",
            reply_markup=keyboard_page
        )
        return
    
    if previous_page:
        previous_page_param = previous_page.split("?")[1]
        callback_data = json.dumps(
            {
                "type": "prev_page_game_search",
                "prev_page": previous_page_param
            }
        )
        previous_page_button = InlineKeyboardButton(
            "❮",
            callback_data=callback_data
        )

        keyboard_page.add(previous_page_button)

        bot.send_message(
            user_chat_id,
            "Previous page",
            reply_markup=keyboard_page
        )
        return
    
    if next_page:
        next_page_param = next_page.split("?")[1]

        callback_data = json.dumps(
            {
                "type": "next_page_game_search",
                "next_page": next_page_param
            }
        )
        next_page_button = InlineKeyboardButton(
            "❯",
            callback_data=callback_data
        )

        keyboard_page.add(next_page_button)
        bot.send_message(
            user_chat_id,
            "Next page",
            reply_markup=keyboard_page
        )
        return

@bot.callback_query_handler(
        func=lambda call: 
        json.loads(call.data).get("type") == "next_page_game_search"
)
def games_search_next_page(call):
    game_search_result(
        None,
        url_param=json.loads(call.data).get("next_page"),
        user_chat_id=call.from_user.id
    )

@bot.callback_query_handler(
        func=lambda call:
        json.loads(call.data).get("type") == "prev_page_game_search"
)
def games_search_previous_page(call):
    game_search_result(
        None,
        url_param=json.loads(call.data).get("prev_page"),
        user_chat_id=call.from_user.id
    )

@bot.callback_query_handler(
        func=lambda call:
        json.loads(call.data).get("type") == "game"
)
def games_info(call):
    game_id = json.loads(call.data).get("game_id")
    r = requests.get(f"http://127.0.0.1:8000/api/v1/games/{game_id}")
    request_data = r.json()

    game = request_data.get("game")
    bot.send_message(call.from_user.id, game.get("name"))

    game_screenshots = []
    
    for screenshot in game.get("screenshot"):
        game_screenshots.append(
            InputMediaPhoto(
                open(
                    BASE_DIR/"media"/screenshot.get("file_url"),
                    "rb"
                )
            )
        )

    bot.send_media_group(
        call.from_user.id,
        game_screenshots
    )

    keyboard = InlineKeyboardMarkup()

    all_handbook = InlineKeyboardButton(
        f"all handbook for {game.get('name')}",
        callback_data=json.dumps(
            {
                "type": "all_handbook",
                "game_id": game_id
            }
        )
    )
    
    keyboard.add(all_handbook)
    bot.send_message(
        call.from_user.id,
        f"All handbook for {game.get('name')}",
        reply_markup=keyboard
    )

bot.infinity_polling()