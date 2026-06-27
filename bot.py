import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "TOKEN_BU_YERDA")
CHANNEL_USERNAME = "@seen_sms"
WEBAPP_URL = "https://akhrorbeksalaydinovuzn-cell.github.io/lotin-miniapp/miniapp.html"

logging.basicConfig(level=logging.INFO)

async def check_subscription(user_id: int, bot) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    is_sub = await check_subscription(user.id, context.bot)

    if not is_sub:
        keyboard = [
            [InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub")]
        ]
        await update.message.reply_text(
            f"👋 Salom, {user.first_name}!\n\n"
            f"⚠️ Botdan foydalanish uchun {CHANNEL_USERNAME} kanaliga obuna bo'ling:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    await send_main_menu(update.message, user.first_name)

async def send_main_menu(message, name=""):
    keyboard = [
        [InlineKeyboardButton(
            "🌐 Lotin.uz Mini Ilovasini Ochish",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
    ]
    await message.reply_text(
        f"👋 Salom{', ' + name if name else ''}!\n\n"
        "🤖 *Lotin.uz* botiga xush kelibsiz!\n\n"
        "Bu bot yordamida:\n"
        "🔄 Lotin ↔ Kirill konvertatsiya\n"
        "🌐 10+ tilda tarjima\n"
        "📄 Fayl konvertatsiyasi\n\n"
        "Quyidagi tugmani bosib mini ilovani oching 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "check_sub":
        is_sub = await check_subscription(query.from_user.id, context.bot)
        if is_sub:
            keyboard = [
                [InlineKeyboardButton(
                    "🌐 Lotin.uz Mini Ilovasini Ochish",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )],
                [InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ]
            await query.message.edit_text(
                "✅ *Obuna tasdiqlandi!*\n\nMini ilovani oching 👇",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
        else:
            keyboard = [
                [InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                [InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub")]
            ]
            await query.message.edit_text(
                f"❌ Hali {CHANNEL_USERNAME} ga obuna bo'lmagansiz.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_sub = await check_subscription(update.effective_user.id, context.bot)
    if not is_sub:
        keyboard = [
            [InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub")]
        ]
        await update.message.reply_text(
            f"⚠️ {CHANNEL_USERNAME} kanaliga obuna bo'ling:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    await send_main_menu(update.message)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
