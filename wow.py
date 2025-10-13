from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from typing import Dict, List

user_id_user: Dict[str, int] = {}
user_user_id: Dict[int, str] = {}
user_sessions: Dict[int, Session] = {}  #user-session
sessions_user: Dict[Session, list] = {} # session-user
global kolvo_user
kolvo_user = 0
global kolvo_session
kolvo_session = 0

async def send_message_to_user(bot, user_id: int, text: str):
    await bot.send_message(chat_id=user_id, text=text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начало работы с ботом"""
    user = update.effective_user
    user_id = user.id
    keyboard = [["✅ Присоединиться к сессии", "🆕 Создать новую сессию"]]
    await update.message.reply_text(
        f"Привет, {user.first_name}! 🎮\nВыберите действие:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id

    session = user_sessions[user_id]
    # Уведомляем всех игроков
    session_users = sessions_user(session)
    for player_number in session_users:
        await send_message_to_user(
            context.bot,
            user_id[player_number],
            f"🚪 Игрок {user.first_name} завершил сессию {session}"
        )

        # Удаляем сессию
    for player_number in session_users:
        del user_id_user[user_user_id[player_number]]
        del user_user_id[player_number]
        del sessions_user[session]
        del user_sessions[player_number]

    await update.message.reply_text(
        f"✅ Сессия {session} удалена!",
        reply_markup=ReplyKeyboardRemove()
    )

async def show_game_interface(update: Update, session: Session, user_id: int):
    player_number = session.get_player_number()
    commands1 = session.get_available_commands1()
    commands2 = session.get_available_commands2()
    commands3 = session.get_available_commands3()
    keyboard1 = [commands1[i:i + 2] for i in range(0, len(commands1), 2)]
    keyboard2 = [commands2[i:i + 2] for i in range(0, len(commands2), 2)]
    keyboard3 = [commands3[i:i + 2] for i in range(0, len(commands3), 2)]

    status_text = f"Сессия {session.session_id}\n"
    status_text += f"Игроков: {len(session.players)}\n"
    status_text += f"Ваш номер: {player_number}\n\n"
    status_text += "Выберите команду:"

    await update.message.reply_text(
        status_text,
        reply_markup=ReplyKeyboardMarkup(keyboard1, resize_keyboard=True)
    )
    status_text = "Выберите команду:"
    await update.message.reply_text(
        status_text,
        reply_markup=ReplyKeyboardMarkup(keyboard2, resize_keyboard=True)
    )
    status_text = "Выберите команду:"
    await update.message.reply_text(
        status_text,
        reply_markup=ReplyKeyboardMarkup(keyboard3, resize_keyboard=True)
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id
    text = update.message.text

    if text == "✅ Присоединиться к сессии":
        await update.message.reply_text(
            "Введите ID сессии:",
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data['awaiting_session_join'] = True

    elif text == "🆕 Создать новую сессию":

        session_id = kolvo_session
        kolvo_session+= 1

        new_session = Session(session_id)

        player_number = kolvo_user
        kolvo_user += 1
        new_session.add_new_player(player_number)#ask position
        user_sessions[player_number] = new_session
        sessions_user[new_session].append(player_number)
        user_user_id[player_number] = user_id
        user_id_user[user_id] = player_number

        await update.message.reply_text(
            f"🎉 Сессия {session_id} создана!\n"
            f"Ваш номер игрока: {player_number}\n"
            f"ID сессии: {session_id}",
            reply_markup=ReplyKeyboardRemove()
        )
        await show_game_interface(update, new_session, user_id)

    elif context.user_data.get('awaiting_session_join'):
        session = int(text)
        player_number = kolvo_user
        kolvo_user += 1
        session.add_new_player(player_number)
        user_sessions[player_number] = session
        sessions_user[session].append(player_number)
        user_user_id[player_number] = user_id
        user_id_user[user_id] = player_number

        await update.message.reply_text(
            f"✅ Вы присоединились к сессии {session}!\n"
            f"Ваш номер игрока: {player_number}",
            reply_markup=ReplyKeyboardRemove()
        )

            # Уведомляем всех о новом игроке
        session_users = sessions_user[session]
        for session_user_id in session_users:
            if session_user_id != user_id:
                await send_message_to_user(
                context.bot,
                session_user_id,
                    f"🎮 Новый игрок {player_number} присоединился к сессии!"
                )

        await show_game_interface(update, session, user_id)
        context.user_data['awaiting_session_join'] = False

        # Обработка игровых команд
        session = user_sessions[user_id]
        player_number = user_id_user[user_id]

        # Отправляем команду в session для обработки
        result_text = session.process_command(player_number, text)

        # Уведомляем всех игроков о результате
        session_users = sessions_user[session]
        for session_user_id in session_users:
            await send_message_to_user(context.bot, session_user_id, result_text)

        # Показываем обновленный интерфейс
        await show_game_interface(update, session, user_id)


def main() -> None:
    """Запуск бота"""
    BOT_TOKEN = "YOUR_BOT_TOKEN"

    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("delete", delete_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()


main()

