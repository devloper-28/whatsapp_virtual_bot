import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)

# Replace 'YOUR_API_TOKEN' with your actual Telegram API token
TOKEN = "6934887290:AAHnfnCD3-KNjjtLWOaaN9NAGvbVPt-J7cc"
QR_CODE_IMAGE_URL = "https://wertrends.s3.eu-north-1.amazonaws.com/Image.jpg"
ADMIN_CHAT_ID = "676637767"
QUERY_LINK12 = "https://www.youtube.com/shorts/wC23vXpE2Hc"
QUERY_LINK123 = "https://skrill.me/rq/PRAJAPATI/650/INR?key=YWpTSOor38Z78Pxepqmb0bESSVq"
QUERY_LINK = "https://t.me/WeRTrends_admin"

APP_NAME = 'https://virtualnumberbot-c60640ab9899.herokuapp.com/'
PORT = int(os.environ.get('PORT', '5000'))

active_users = {}

# Set up logging
logging.basicConfig(
    filename="transaction.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton(
                "Get Virtual Number", callback_data="get_virtual_number"
            )
        ],
        [
            InlineKeyboardButton(
                "🅿Pay via Paypal🅿", url="https://www.paypal.me/BadalPrajapati"
            )
        ],
        [
            InlineKeyboardButton(
                "🌐Pay International🌐",
                url="https://skrill.me/rq/Badal/650/INR?key=CShvFQ-cnsD4PKxW4jekpUQ44sC",
            )
        ],
        [InlineKeyboardButton("💰Pay via Crypto💰", callback_data="pay_via_crypto")],
        [InlineKeyboardButton("Contact Support", url="https://t.me/WeRTrends_admin")],
        [
            InlineKeyboardButton(
                "How to use this bot", url="https://www.youtube.com/shorts/wC23vXpE2Hc"
            )
        ],
        [
            InlineKeyboardButton(
                "Provide Feedback of service", url="https://forms.gle/8Rbi1t49ZkbiRuqy7"
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_photo(
        photo=QR_CODE_IMAGE_URL,
        caption=f"Welcome to the bot!\n\n"
        f"Please pay 650rs to receive a virtual number.\n\n"
        f"Scan the QR code above to make the payment and don't forget to send the transaction ID.\n\n"
        f"If you are facing any difficulties, please raise your query [Click Here]({QUERY_LINK})."
        f"\n\nPlease note that the transaction ID is mandatory for processing."
        f"\n\nOnce you provide transaction ID, We will give you virtual number and also Let us know for which app you are trying to sign up. I will give you OTP."
        f"\n\nHOW TO USE BOT LINK.[Click Here]({QUERY_LINK12}).",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


def forward_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    user_id = update.message.from_user.id

    # Notify the admin with the user's ID and message
    admin_notification = f"From: {user_name} (ID: {user_id})\n\n{user_message}"
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_notification)

    # Send a separate message containing just the user's ID
    user_id_message = f"/reply {user_id}"
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=user_id_message)

    if str(chat_id) != ADMIN_CHAT_ID:
        active_users[update.message.from_user.username] = chat_id

    if str(chat_id) != ADMIN_CHAT_ID:
        forwarded_message = f"From: {user_name} (ID: {user_id})\n\n{user_message}"
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=forwarded_message)


def receive_photo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if str(chat_id) != ADMIN_CHAT_ID:
        active_users[update.message.from_user.username] = chat_id

    file_id = update.message.photo[-1].file_id
    photo_obj = context.bot.get_file(file_id)
    photo_obj.download("received_photo.jpg")

    admin_message = f"Received photo from user {update.message.from_user.first_name} (ID: {update.message.from_user.id})"
    context.bot.send_photo(
        chat_id=ADMIN_CHAT_ID, photo=photo_obj.file_id, caption=admin_message
    )

    update.message.reply_text(
        "Thank you for the photo!, You will get confirmation soon with our team"
    )


def list_users(update: Update, context: CallbackContext):
    user_list = "\n".join(
        [f"{user}: {chat_id}" for user, chat_id in active_users.items()]
    )
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Active users:\n{user_list}")


def admin_reply(update: Update, context: CallbackContext):
    try:
        parts = update.message.text.split(" ", 2)
        user_chat_id = int(parts[1].strip())
        reply_message = parts[2].strip()

        if reply_message:
            context.bot.send_message(chat_id=user_chat_id, text=reply_message)
        else:
            update.message.reply_text(
                "Message cannot be empty. Please provide a valid message."
            )
    except (ValueError, IndexError) as e:
        update.message.reply_text(
            f"Error: {e}. Invalid format. Please use: '/reply user_chat_id: Your reply message'"
        )

    logging.info(
        f"Parsed parts: {parts}, User chat ID: {user_chat_id}, Reply message: {reply_message}"
    )


def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "get_virtual_number":
        query.message.reply_text(
            "Please pay 650rs to get a virtual number. If you have already paid, please provide a screenshot so we can confirm and give you the virtual number."
        )
    elif query.data == "pay_via_crypto":
        crypto_keyboard = [
            [InlineKeyboardButton("TRX", callback_data="crypto_trx")],
            [InlineKeyboardButton("USDT - BEP20", callback_data="crypto_usdt_bep20")],
            [InlineKeyboardButton("USDT - ERC20", callback_data="crypto_usdt_erc20")],
            [InlineKeyboardButton("USDT TRC20", callback_data="crypto_usdt_trc20")],
            [InlineKeyboardButton("BTC", callback_data="crypto_btc")],
            [InlineKeyboardButton("Back", callback_data="back")],
        ]
        crypto_markup = InlineKeyboardMarkup(crypto_keyboard)
        query.message.reply_text(
            "Please select the cryptocurrency you want to pay with:",
            reply_markup=crypto_markup,
        )
    elif query.data == "back":
        # Send the main menu again
        start(update.callback_query, context)
    elif query.data == "crypto_trx":
        query.message.reply_text("TRX Address: TFGR4bLURdHXXP64pA8sAV6j4M3Us4Un8E")
    elif query.data == "crypto_usdt_bep20":
        query.message.reply_text(
            "USDT - BEP20 Address: 0x0c2c298dF964088D71FCAc7C625eb36E420BA1B2"
        )
    elif query.data == "crypto_usdt_erc20":
        query.message.reply_text(
            "USDT - ERC20 Address: 0x0c2c298dF964088D71FCAc7C625eb36E420BA1B2"
        )
    elif query.data == "crypto_usdt_trc20":
        query.message.reply_text(
            "USDT TRC20 Address: TFGR4bLURdHXXP64pA8sAV6j4M3Us4Un8E"
        )
    elif query.data == "crypto_btc":
        query.message.reply_text(
            "BTC Address: bc1qqqyqwk7dz47u284hlaxm22ssvl64uzr94utvcm"
        )


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))
    dp.add_handler(MessageHandler(Filters.photo, receive_photo))
    dp.add_handler(CommandHandler("listusers", list_users))
    dp.add_handler(CommandHandler("reply", admin_reply))
    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME+TOKEN)
    updater.idle()


if __name__ == "__main__":
    main()
