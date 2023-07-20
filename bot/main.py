import os
import requests
from config import (
    STATES,
    URL_API,
    BASE_DIR,
    BOT_TOKEN,
)
from telegram import (
    Update,
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
        global game_list_prev_page
        game_list_prev_page = prev_page

        callback_data = "game_list_prev_page"
        
        page_button.append(
            InlineKeyboardButton("❮", callback_data=callback_data)
        )
        
    if next_page:        
        global game_list_next_page
        game_list_next_page = next_page

        callback_data = "game_list_next_page"
        
        page_button.append(
            InlineKeyboardButton("❯", callback_data=callback_data)
        )

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
        url=game_list_next_page)
    
async def game_list_prev_page(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):
    
    await game_list(
        update=update, context=context,
        url=game_list_prev_page
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
            pattern="game_list_next_page"
        )
    )
    
    app.add_handler(
        CallbackQueryHandler(
            game_list_prev_page,
            pattern="game_list_prev_page"
        )
    )

    app.run_polling()

if __name__ == "__main__":
    main()