import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

class bot:
    def __init__(self, token, handler_cb = None):
        if token == '':
            logging.error('token is empty')
            self.application = None
        else:
            self.application = ApplicationBuilder().token(token).build()

        self.handler_cb = handler_cb

    def start(self):
        if self.application == None:
            return

        logging.info('bot start running...')
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.run_polling()

    async def stop(self):
        if self.application == None:
            return

        logging.info('bot stop running...')
        await self.application.updater.stop()
        await self.application.stop()

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        logging.info(f"received message: {user_message}")
        if self.handler_cb == None:
            new_msg = user_message
        else:
            new_msg = self.handler_cb(user_message)
        await update.message.reply_text(new_msg, reply_to_message_id=update.message.message_id)

    async def send(self, who, context=None, image=None):
        if self.application == None:
            return

        try:
            if image != None:
                await self.application.bot.send_photo(
                    chat_id    = who,
                    photo      = image,
                    caption    = context,
                    parse_mode = 'MarkdownV2',
                )
            else:
                await self.application.bot.send_message(
                    chat_id                  = who,
                    text                     = context,
                    disable_web_page_preview = True,
                    parse_mode               = 'MarkdownV2',
                )

        except Exception as e:
            logging.error(f'sending message failed: {e}')
