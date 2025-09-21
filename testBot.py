from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import dotenv
import requests

dotenv.load_dotenv()
TOKEN = dotenv.dotenv_values().get('TOKEN')
URL_SHEET = dotenv.dotenv_values().get('URL_SHEET')

def save_to_sheet(user, text):
    try:
        data = {
            "user": user,
            "text": text
        }
        if not URL_SHEET:
            print("URL_SHEET tidak ditemukan di file .env.")
            return False
        
        response = requests.post(URL_SHEET, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengirim data ke spreadsheet: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirimkan pesan apa saja, dan saya akan menyimpannya.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username or update.message.from_user.first_name
    text = update.message.text
    
    if save_to_sheet(user, text):
        await update.message.reply_text("Pesan Anda telah berhasil disimpan!")
    else:
        await update.message.reply_text("Terjadi kesalahan saat menyimpan pesan.")

def main():
    if not TOKEN:
        print("TOKEN tidak ditemukan di file .env. Bot tidak bisa dijalankan.")
        return
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()