from telegram.ext import CommandHandler, CallbackQueryHandler
from bot.start import (
    start_command,
    help_callback,
    back_to_start,
    help_2,
    close_help,
)
from bot.challenge import challenge_command, button_callback
from bot.game import game_button_callback
from bot.score import myscore_command, topscore_command

def register_handlers(app):
    # ✅ Command Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_callback))
    app.add_handler(CommandHandler("challenge", challenge_command))
    app.add_handler(CommandHandler("myscore", myscore_command))
    app.add_handler(CommandHandler("topscore", topscore_command))

    # ✅ Callback Query Handlers for Game
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^(confirm|cancel)_"))
    app.add_handler(CallbackQueryHandler(game_button_callback, pattern="^move_"))

    # ✅ Callback Query Handlers for UI
    app.add_handler(CallbackQueryHandler(help_callback, pattern="^help_commands$"))       # DM Help
    app.add_handler(CallbackQueryHandler(help_2, pattern="^group_help$"))                 # Group Help
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="^start_back$"))          # DM back to start
    app.add_handler(CallbackQueryHandler(close_help, pattern="^close_help$"))             # Group help close
