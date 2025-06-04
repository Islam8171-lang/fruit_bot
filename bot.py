from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)

BOT_TOKEN = "7163340236:AAFae9HD45xQbD0dG1ueI4eJMRvL5IYKFGk"
ADMIN_ID = 417731116

# Состояния
QUESTION, ORDER = range(2)

# Главное меню
def main_menu_keyboard():
    return ReplyKeyboardMarkup([
        ["Товары и цены", "Доставка"],
        ["Наш адрес", "Сделать заказ"],
        ["Задать вопрос?"]
    ], resize_keyboard=True)

# Меню "Назад"
back_menu = ReplyKeyboardMarkup([["Назад"]], resize_keyboard=True)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Здравствуйте, {user_first_name}! \nРады, что вы интересуетесь нашими товарами.\nУ нас также работает доставка.\n\nВыберите интересующую вас информацию:",
        reply_markup=main_menu_keyboard()
    )

# Обработка кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Товары и цены":
        await update.message.reply_text(
            "Прайс на наши товары:\n"
            "\nТомат жёлтый (Польша) 18р/кг"
            "\nТомат розовый (Азербайджан) 15.50р/кг"
            "\nПерец жёлтый (Азербайджан) 14р/кг"
            "\nПерец красный (Азербайджан) 14р/кг"
            "\nОгурец короткоплодный колючий (РФ) 7.2р/кг"
            "\nОгурец Зозуля (РБ) 6.5р/кг"
            "\nКартофель молодой (Азербайджан) 5.50р/кг"
            "\nРедис (РФ) 6.50р/кг"
            "\nКлубника Азия (РБ) 20р/кг"
            "\nКлубника Альба (РБ) 25р/кг"
            "\nЧерешня (Узбекистан) 25р/кг"
            "\nКапуста молодая (РФ) 4.50р/кг"
            "\nДыня (Туркменистан) 10.50р/кг"
            "\nАрбуз (Иран) 6.50р/кг",
            reply_markup=back_menu
        )
    elif text == "Доставка":
        await update.message.reply_text(
            "Условия доставки:\n"
            "Доставляем наши фрукты от 40 до 100 рублей бесплатно\n"
            "в пределах 20 км от нашей точки!",
            reply_markup=back_menu
        )
    elif text == "Наш адрес":
        await update.message.reply_text(
            "Наш адрес: Логойская, улица 5А, Валерьяново, Минская область",
            reply_markup=back_menu
        )
    elif text == "Назад":
        await update.message.reply_text("Вы вернулись в главное меню.", reply_markup=main_menu_keyboard())
    elif text == "Задать вопрос?":
        await update.message.reply_text("Напишите ваш вопрос, и мы скоро ответим:")
        return QUESTION
    elif text == "Сделать заказ":
        await update.message.reply_text("Пожалуйста, введите ваш заказ (Имя, Телефон, Адрес):")
        return ORDER
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки ниже.", reply_markup=main_menu_keyboard())

# Получение вопроса
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"❓ Новый вопрос от {user.full_name} (@{user.username or 'без ника'}):\n\n{message}"
    )
    await update.message.reply_text("Спасибо! Ваш вопрос отправлен. Мы скоро свяжемся с вами.", reply_markup=main_menu_keyboard())
    return ConversationHandler.END

# Получение заказа
async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🛒 Новый заказ от {user.full_name} (@{user.username or 'без ника'}):\n\n{message}"
    )
    await update.message.reply_text("Спасибо за заказ! Мы скоро с вами свяжемся.", reply_markup=main_menu_keyboard())
    return ConversationHandler.END

# /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Действие отменено.", reply_markup=main_menu_keyboard())
    return ConversationHandler.END

# Запуск
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Обработка вопросов
    question_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Задать вопрос\?$"), handle_message)],
        states={
            QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # Обработка заказов
    order_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Сделать заказ$"), handle_message)],
        states={
            ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(question_conv)
    app.add_handler(order_conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
