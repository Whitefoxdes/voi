import os
import requests
from config import (
    STATES,
    URL_API,
    BASE_DIR,
    BOT_TOKEN,
    MEDIA_DIR
)
from telegram import (
    Update,
    InputMediaPhoto,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    filters,
    ContextTypes,
    CommandHandler, 
    MessageHandler,
    ApplicationBuilder,
    ConversationHandler,
    CallbackQueryHandler
)

async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Hello, this'xis VOI bot")

async def game_search(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Write game name, like this: Skyrim, Prey, Dishonored")

    return STATES["GAME_SEARCH"]

async def game_list(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        url=None):

    if update.callback_query:
        query = update.callback_query
        await query.answer()
    else:
        query = None

    if url:
        request_url = f"{url}"
    else: 
        name = update.message.text
        request_url = f"{URL_API}games/search/?name={name}"

    request = requests.get(request_url)
    request_data = request.json()

    games = request_data.get("results")
    prev_page = request_data.get("previous")
    next_page = request_data.get("next")

    game_button = []
    
    global game_id_list
    
    game_id_list = {}
    game_button_index = 0

    for game in games:
        callback_data = f"game_info_{game_button_index}"
        game_button.append(
            [
                InlineKeyboardButton(
                    game.get("name"),
                    callback_data=callback_data
                )
            ]
        )
        game_id_list[callback_data] = game.get("id")
        game_button_index += 1

    keyboard_game = InlineKeyboardMarkup(game_button)
    if query:
        await query.message.reply_text(
            "Game list",
            reply_markup=keyboard_game
        )
    else:
        await update.message.reply_text(
            "Game list",
            reply_markup=keyboard_game
        )
    page_button = []
    if prev_page:
        global game_list_prev_page_url
        game_list_prev_page_url = prev_page

        callback_data = "game_list_prev_page"

        page_button.append(
            InlineKeyboardButton("❮", callback_data=callback_data)
        )

    if next_page:
        global game_list_next_page_url
        game_list_next_page_url = next_page

        callback_data = "game_list_next_page"

        page_button.append(
            InlineKeyboardButton("❯", callback_data=callback_data)
        )
    if not page_button:
        return ConversationHandler.END

    keyboard_page = InlineKeyboardMarkup([page_button])

    if query:
        await query.message.reply_text(
            "Select page",
            reply_markup=keyboard_page
        )
    else:
        await update.message.reply_text(
            "Select page",
            reply_markup=keyboard_page
        )
    return ConversationHandler.END


async def game_list_next_page(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    await game_list(
        update=update, context=context,
        url=game_list_next_page_url)

async def game_list_prev_page(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    await game_list(
        update=update, context=context,
        url=game_list_prev_page_url
    )

async def game_info(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    global game_id
    game_id = game_id_list.get(query.data)

    request_url = f"{URL_API}games/{game_id}"
    request = requests.get(request_url)
    request_data = request.json()

    game = request_data.get("game")
    await query.message.reply_text(
        game.get("name")
    )
    screenshot_list = []
    for screenshot in game.get("screenshot"):
        if len(screenshot_list) == 10:
            await query.message.reply_media_group(
                screenshot_list
            )

        file_url = screenshot.get("file_url")
        screenshot_list.append(
            InputMediaPhoto(
                open(MEDIA_DIR/file_url, "rb")
            )
        )
    await query.message.reply_media_group(
        screenshot_list
    )
    callback_data = "handbook_list"
    all_handbook_button = [
        InlineKeyboardButton(
            f"Get all handbook for {game.get('name')}",
            callback_data=callback_data
        )
    ]
    keyboard_all_handbook = InlineKeyboardMarkup(
        [all_handbook_button]
    )
    await query.message.reply_text(
        f"All handbook for {game.get('name')}",
        reply_markup=keyboard_all_handbook
    )

async def handbook_list(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        url=None):
    
    query = update.callback_query
    
    if url:
        request_url = f"{url}"
    else:
        request_url = f"{URL_API}handbook/handbook-list/?game={game_id}"

    request = requests.get(request_url)
    request_data = request.json()

    handbooks = request_data.get("results")
    prev_page = request_data.get("previous")
    next_page = request_data.get("next")

    handbook_button = []
    global handbook_id_list
    handbook_id_list = {}
    handbook_button_index = 0
    
    for handbook in handbooks:
        callback_data = f"handbook_info_{handbook_button_index}"
        handbook_button.append(
            [
                InlineKeyboardButton(
                    handbook.get("title"),
                    callback_data=callback_data
                )
            ]
        )
        handbook_id_list[callback_data] = handbook.get("id")
        handbook_button_index += 1

    keyboard_handbook = InlineKeyboardMarkup(handbook_button)
    await query.message.reply_text(
        "Handbook list",
        reply_markup=keyboard_handbook
    )
    page_button = []
    if prev_page:
        global handbook_list_prev_page_url
        handbook_list_prev_page_url = prev_page

        callback_data = "handbook_list_prev_page"

        page_button.append(
            InlineKeyboardButton("❮", callback_data=callback_data)
        )

    if next_page:
        global handbook_list_next_page_url
        handbook_list_next_page_url = next_page

        callback_data = "handbook_list_next_page"

        page_button.append(
            InlineKeyboardButton("❯", callback_data=callback_data)
        )

    keyboard_page = InlineKeyboardMarkup([page_button])

    await query.message.reply_text(
        "Select page",
        reply_markup=keyboard_page
    )
    # return

async def handbook_list_next_page(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):
    await handbook_list(
        update=update, context=context,
        url=handbook_list_next_page_url)

async def handbook_list_prev_page(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):
    await handbook_list(
        update=update, context=context,
        url=handbook_list_prev_page_url
    )

async def cancel(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    await update.message.reply_text(
        "Cancel this process"
    )

    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    game_search_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("gamesearch", game_search)
        ],
        states={
            STATES["GAME_SEARCH"]: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    game_list
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    app.add_handler(CommandHandler("start", start))

    app.add_handler(game_search_conv_handler)

    app.add_handler(
        CallbackQueryHandler(
            game_list_next_page,
            pattern="^" + "game_list_next_page" + "$"
        )
    )
    app.add_handler(
        CallbackQueryHandler(
            game_list_prev_page,
            pattern="^" + "game_list_prev_page" + "$"
        )
    )
    app.add_handler(
        CallbackQueryHandler(
            game_info,
            pattern=r"game_info_[0-9]{1}"
        )
    )
    app.add_handler(
        CallbackQueryHandler(
            handbook_list,
            pattern="^" + "handbook_list" + "$"
        )
    )
    app.add_handler(
        CallbackQueryHandler(
            handbook_list_next_page,
            pattern="^" + "handbook_list_next_page" + "$"
        )
    )
    app.add_handler(
        CallbackQueryHandler(
            handbook_list_prev_page,
            pattern="^" +"handbook_list_prev_page" + "$"
        )
    )
    app.run_polling()

if __name__ == "__main__":
    main()