import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('static/welcome.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)

	# keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("🎲 Будь яке число")
	item2 = types.KeyboardButton("😊 Будь яка емоція?")

	markup.add(item1, item2)

	bot.send_message(message.chat.id, "Доброго дня, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		if message.text == '🎲 рандомне число':
			bot.send_message(message.chat.id, str(random.randint(0,100)))
		elif message.text == '😊 Як справи?':

			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton("Добре", callback_data='good')
			item2 = types.InlineKeyboardButton("Не дуже", callback_data='bad')

			markup.add(item1, item2)

			bot.send_message(message.chat.id, 'Класно, як сам?', reply_markup=markup)
		else:
			bot.send_message(message.chat.id, 'Я не знаю що відповісти')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'good':
				bot.send_message(call.message.chat.id, 'Ура)')
			elif call.data == 'bad':
				bot.send_message(call.message.chat.id, 'Буває(')

			# remove inline buttons
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
				reply_markup=None)

			# show alert
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text="Це тестове повідомлення!!11")

	except Exception as e:
		print(repr(e))

# RUN
bot.polling(none_stop=True)