from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

active_games = {}

def build_board(board, turn_user_id):
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            value = board[i][j] or "➖"
            row.append(InlineKeyboardButton(value, callback_data=f"move_{i}_{j}_{turn_user_id}"))
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)

def check_winner(board):
    lines = board + list(zip(*board)) + [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]
    for line in lines:
        if line[0] and all(cell == line[0] for cell in line):
            return line[0]
    return None

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE, player1, player2):
    board = [["" for _ in range(3)] for _ in range(3)]
    active_games[update.effective_chat.id] = {
        "board": board,
        "turn": player1.id,
        "players": {player1.id: "❌", player2.id: "⭕"},
        "ids": (player1.id, player2.id),
        "usernames": (player1.mention_html(), player2.mention_html())
    }

    await update.effective_chat.send_message(
        f"🎮 Game started! {player1.mention_html()} (❌) vs {player2.mention_html()} (⭕)",
        reply_markup=build_board(board, player1.id),
        parse_mode="HTML"
    )

async def game_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    if chat_id not in active_games:
        await query.answer("❌ No active game.")
        return

    game = active_games[chat_id]
    if user_id != game["turn"]:
        await query.answer("⏳ Not your turn.")
        return

    _, row, col, _ = query.data.split("_")
    row, col = int(row), int(col)

    if game["board"][row][col]:
        await query.answer("❌ Already taken.")
        return

    symbol = game["players"][user_id]
    game["board"][row][col] = symbol

    winner = check_winner(game["board"])
    if winner:
        await query.edit_message_text(f"🏆 {query.from_user.mention_html()} wins!", parse_mode="HTML")
        del active_games[chat_id]
        return

    if all(cell for row in game["board"] for cell in row):
        await query.edit_message_text("🤝 It's a draw!")
        del active_games[chat_id]
        return

    next_turn = [uid for uid in game["ids"] if uid != user_id][0]
    game["turn"] = next_turn

    await query.edit_message_text(
        f"🎯 Turn: {game['usernames'][game['ids'].index(next_turn)]}",
        reply_markup=build_board(game["board"], next_turn),
        parse_mode="HTML"
             )
