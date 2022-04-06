from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_Graphics = KeyboardButton("/Graphics")
button_Text = KeyboardButton("/Text")
button_info = KeyboardButton("/Info")

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(button_Graphics, button_Text, button_info)
