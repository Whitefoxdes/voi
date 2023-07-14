import os
import sys
import json
import telebot
import requests
from urllib.parse import (
    parse_qs,
    urlparse
)
from telebot.types import (
    InputMediaPhoto,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from voi.settings import (
    BASE_DIR,
    BOT_TOKEN
)

bot = telebot.TeleBot(BOT_TOKEN)

callback_data_filter = {
    "next_page_games_search": "npgs",
    "prev_page_games_search": "ppgs",
    "game_info": "gi",
    "next_page_all_game": "npag",
    "prev_page_all_game": "ppag",
    "all_handbook": "ah",
    "handbook_type_list": "htl",
    "next_page_all_handbook": "npah",
    "prev_page_all_handbook": "ppah",
    "handbook_info": "hi",
}

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
            user_chat_id,
            "Game not found, write another game name"
        )
        bot.register_next_step_handler(
            error_game_not_found_msg,
            game_search_result,
            user_chat_id=user_chat_id 
        )
        return

    previous_page = request_data.get("previous")
    next_page = request_data.get("next")

    keyboard = InlineKeyboardMarkup()
    keyboard_page = InlineKeyboardMarkup()

    for game in results:
        callback_data = json.dumps(
            {
              "f": callback_data_filter["game_info"],
              "g": game.get('id')
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
        previous_page_param = urlparse(previous_page).query
        next_page_param = urlparse(next_page).query

        pp_parse_qs = parse_qs(previous_page_param)
        np_parse_qs = parse_qs(next_page_param)

        if pp_parse_qs.get("page"):
            pp_number = int(pp_parse_qs.get("page")[0])
        else:
            pp_number = None
            
        np_number = int(np_parse_qs.get("page")[0])
        
        previous_page_callback_data = json.dumps(
            {
                "f": callback_data_filter["prev_page_games_search"],
                "n": pp_parse_qs.get("name")[0],
                "p": pp_number
            }
        )
        next_page_callback_data = json.dumps(
            {
                "f": callback_data_filter["next_page_games_search"],
                "n": np_parse_qs.get("name")[0],
                "p": np_number
            }
        )
        previous_page_button = InlineKeyboardButton(
            "❮",
            callback_data=previous_page_callback_data
        )
        if len(next_page_callback_data) > 64:
            keyboard_page.add(previous_page_button)
            bot.send_message(
                user_chat_id,
                "Previous page",
                reply_markup=keyboard_page
            )
            error_next_page_forbidden = bot.send_message(
                user_chat_id,
                "Next page forbidden http://127.0.0.1:8000"
            )
            return
        
        next_page_button = InlineKeyboardButton(
            "❯",
            callback_data=next_page_callback_data
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
        previous_page_param = urlparse(previous_page).query
        pp_parse_qs = parse_qs(previous_page_param)
        
        if pp_parse_qs.get("page"):
            pp_number = int(pp_parse_qs.get("page")[0])
        else:
            pp_number = None

        callback_data = json.dumps(
            {
                "f": callback_data_filter["prev_page_games_search"],
                "n": pp_parse_qs.get("name")[0],
                "p": pp_number
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
        next_page_param = urlparse(next_page).query
        np_parse_qs = parse_qs(next_page_param)
        page_number = int(np_parse_qs.get("page")[0])
        callback_data = json.dumps(
            {
                "f": callback_data_filter["next_page_games_search"],
                "n": np_parse_qs.get("name")[0],
                "p": page_number
            }
            
        )
        if len(callback_data) > 64:
            error_next_page_forbidden = bot.send_message(
                user_chat_id,
                "Next page forbidden http://127.0.0.1:8000"
            )
            return
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
    json.loads(call.data).get("f") == callback_data_filter["next_page_games_search"]
)
def games_search_next_page(call):
    data = json.loads(call.data)
    game_name = data.get('n')
    page_number = data.get('p')
    url_param = f"name={game_name}&page={page_number}"
    game_search_result(
        None,
        url_param=url_param,
        user_chat_id=call.from_user.id
    )

@bot.callback_query_handler(
    func=lambda call:
    json.loads(call.data).get("f") == callback_data_filter["prev_page_games_search"]
)
def games_search_previous_page(call):
    data = json.loads(call.data)
    game_name = data.get('n')
    page_number = data.get('p')
    if page_number:
        url_param = f"name={game_name}&page={page_number}"
    else:
        url_param = f"name={game_name}"
    game_search_result(
        None,
        url_param=url_param,
        user_chat_id=call.from_user.id
    )

@bot.callback_query_handler(
    func=lambda call:
    json.loads(call.data).get("f") == callback_data_filter["game_info"]
)
def games_info(call):
    game_id = json.loads(call.data).get("g")
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
                "f": callback_data_filter["all_handbook"],
                "g": game_id
            }
        )
    )

    keyboard.add(all_handbook)
    bot.send_message(
        call.from_user.id,
        f"All handbook for {game.get('name')}",
        reply_markup=keyboard
    )

@bot.callback_query_handler(
    func=lambda call:
    json.loads(call.data).get("f") == callback_data_filter["all_handbook"]
)
def all_handbook(
    call=None,
    url_param=None,
    user_chat_id=None
):
    if url_param:
        requests_url = f"http://127.0.0.1:8000/api/v1/handbook/handbook-list/?{url_param}"
    else:
        game_id = json.loads(call.data).get("g")
        requests_url = f"http://127.0.0.1:8000/api/v1/handbook/handbook-list/?game={game_id}"
    
    if not user_chat_id:
        user_chat_id = call.from_user.id

    r_handbook = requests.get(requests_url)
    request_data_handbook = r_handbook.json()

    results = request_data_handbook.get("results")
    previous_page = request_data_handbook.get("previous")
    next_page = request_data_handbook.get("next")

    keyboard_handbook = InlineKeyboardMarkup()
    keyboard_type = InlineKeyboardMarkup()
    keyboard_page = InlineKeyboardMarkup()

    for handbook in results:
        handbook_id = handbook.get("id")
        handbook_title = handbook.get("title")
        callback_data = json.dumps(
            {
                "f": callback_data_filter["handbook_info"],
                "h": handbook_id
            }
        )
        handbook_info_button = InlineKeyboardButton(
            handbook_title,
            callback_data=callback_data
        )
        keyboard_handbook.add(handbook_info_button)
    bot.send_message(
        user_chat_id,
        "Get handbook info",
        reply_markup=keyboard_handbook
    )

    r_handbook_type = requests.get("http://127.0.0.1:8000/api/v1/handbook/handbook-type-list")
    request_data_handbook_type = r_handbook_type.json()

    for handbook_type in request_data_handbook_type:
        requests_url_param = urlparse(requests_url).query
        requests_url_parse_qs = parse_qs(requests_url_param)
        type_id = handbook_type.get("id")

        callback_data = json.dumps(
            {
                "f": callback_data_filter["handbook_type_list"],
                "g": int(requests_url_parse_qs.get("game")[0]),
                "t": type_id
            }
        )
        handbook_type_button = InlineKeyboardButton(
            handbook_type.get("type_name"),
            callback_data=callback_data
        )
        keyboard_type.add(handbook_type_button)
    bot.send_message(
        user_chat_id,
        "Select handbook type",
        reply_markup=keyboard_type
    )

    if next_page and previous_page:
        previous_page_param = urlparse(previous_page).query
        next_page_param = urlparse(next_page).query
        requests_url_param = urlparse(requests_url).query
        
        pp_parse_qs = parse_qs(previous_page_param)
        np_parse_qs = parse_qs(next_page_param)
        requests_url_parse_qs = parse_qs(requests_url_param)

        if pp_parse_qs.get("page"):
            pp_number = int(pp_parse_qs.get("page")[0])
        else:
            pp_number = None

        np_number = np_parse_qs.get("page")[0]

        if requests_url_parse_qs.get("type"):
            url_type_id = int(requests_url_parse_qs.get("type")[0])
        else:
            url_type_id = None

        previous_page_callback_data = json.dumps(
            {
                "f": callback_data_filter["prev_page_all_handbook"],
                "g": int(pp_parse_qs.get("game")[0]),
                "p": pp_number,
                "t": url_type_id
            }
        )
        next_page_callback_data = json.dumps(
            {
                "f": callback_data_filter["next_page_all_handbook"],
                "g": int(np_parse_qs.get("game")[0]),
                "p": np_number,
                "t": url_type_id
            }
        )
        previous_page_button = InlineKeyboardButton(
            "❮",
            callback_data=previous_page_callback_data
        )

        if len(next_page_callback_data) > 64:
            keyboard_page.add(previous_page_button)
            bot.send_message(
                user_chat_id,
                "Previous page",
                reply_markup=keyboard_page
            )
            error_next_page_forbidden = bot.send_message(
                user_chat_id,
                "Next page forbidden http://127.0.0.1:8000"
            )
            return

        next_page_button = InlineKeyboardButton(
            "❯",
            callback_data=next_page_callback_data
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
        previous_page_param = urlparse(previous_page).query
        requests_url_param = urlparse(requests_url).query

        pp_parse_qs = parse_qs(previous_page_param)
        requests_url_parse_qs = parse_qs(requests_url_param)

        if pp_parse_qs.get("page"):
            pp_number = int(pp_parse_qs.get("page")[0])
        else:
            pp_number = None

        if requests_url_parse_qs.get("type"):
            url_type_id = int(requests_url_parse_qs.get("type")[0])
        else:
            url_type_id = None

        callback_data = json.dumps(
            {
                "f": callback_data_filter["prev_page_all_handbook"],
                "g": int(pp_parse_qs.get("game")[0]),
                "p": pp_number,
                "t": url_type_id
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
        next_page_param = urlparse(next_page).query
        requests_url_param = urlparse(requests_url).query

        np_parse_qs = parse_qs(next_page_param)
        requests_url_parse_qs = parse_qs(requests_url_param)
        
        np_number = int(np_parse_qs.get("page")[0])

        if requests_url_parse_qs.get("type"):
            url_type_id = int(requests_url_parse_qs.get("type")[0])
        else:
            url_type_id = None

        callback_data = json.dumps(
            {
                "f": callback_data_filter["next_page_all_handbook"],
                "g": int(np_parse_qs.get("game")[0]),
                "p": np_number,
                "t": url_type_id
            }
        )
        if len(callback_data) > 64:
            error_next_page_forbidden = bot.send_message(
                user_chat_id,
                "Next page forbidden http://127.0.0.1:8000"
            )
            return
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
    json.loads(call.data).get("f") == callback_data_filter["handbook_type_list"]
)
def select_handbook_type(call):
    data = json.loads(call.data)
    game_id = data.get('g')
    handbook_type = data.get('t')
    url_param = f"game={game_id}&type={handbook_type}"
    all_handbook(
        None,
        url_param=url_param,
        user_chat_id=call.from_user.id
    )

@bot.callback_query_handler(
    func=lambda call: 
    json.loads(call.data).get("f") == callback_data_filter["next_page_all_handbook"]
)
def all_handbook_next_page(call):
    data = json.loads(call.data)
    
    game_id = data.get('g')
    page_number = data.get('p')
    url_param = f"game={game_id}&page={page_number}"
    
    if data.get('t'):
        handbook_type = data.get('t')
        url_param += f"&type={handbook_type}"
    all_handbook(
        None,
        url_param=url_param,
        user_chat_id=call.from_user.id
    )

@bot.callback_query_handler(
    func=lambda call:
    json.loads(call.data).get("f") == callback_data_filter["prev_page_all_handbook"]
)
def all_handbook_previous_page(call):
    data = json.loads(call.data)
    
    game_id = data.get('g')
    page_number = data.get('p')
    url_param = f"game={game_id}"
    
    if page_number:
        url_param += f"&page={page_number}"
    if data.get('t'):
        handbook_type = data.get('t')
        url_param += f"&type={handbook_type}"
    all_handbook(
        None,
        url_param=url_param,
        user_chat_id=call.from_user.id
    )
bot.infinity_polling()