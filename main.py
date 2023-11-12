from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler
from pytube import YouTube


def download(link, is_audio):
    try:
        video = YouTube(link)
        video.streams.filter(
            file_extension='mp4', only_audio=is_audio).first().download(filename="video.mp4")
        print("The video is downloaded successfully.")
    except KeyError:
        print("Please check the video URL or your network connection.")


async def dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    download(update.message.text, False)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="downloaded")
    await context.bot.send_video(chat_id=update.effective_chat.id, video=open('video.mp4', 'rb'))



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="start")

if __name__ == '__main__':
    application = ApplicationBuilder().token(
        'TOKEN').build()
    dialog_handler = MessageHandler(filters=None, callback=dialog)
    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)
    application.add_handler(dialog_handler)
    application.run_polling()

