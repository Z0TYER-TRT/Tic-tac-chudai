from telegram.ext import CommandHandler, CallbackQueryHandler
from bot.start import (
    start_command,
    help_callback,
    back_to_start,
)
from bot.challenge import challenge_command, button_callback
from bot.game import game_button_callback
from bot.score import myscore_command, topscore_command

def register_handlers(app):
    # ✅ Standard Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_callback))
    app.add_handler(CommandHandler("challenge", challenge_command))
    app.add_handler(CommandHandler("myscore", myscore_command))
    app.add_handler(CommandHandler("topscore", topscore_command))

    # ✅ Game-specific Callbacks
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^(confirm|cancel)_"))
    app.add_handler(CallbackQueryHandler(game_button_callback, pattern="^move_"))

    # ✅ Bot UI Navigation Callbacks
    app.add_handler(CallbackQueryHandler(help_callback, pattern="^help_commands$"))       # DM Help
    app.add_handler(CallbackQueryHandler(help_2, pattern="^group_help$"))                 # Group Help
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="^start_back$"))          # Back button in DM
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="^close_help$"))          # Close button in group
