import asyncio

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '6391076892:AAGwQHQMKEBAycF_GSrU_r0Zr3-kVCyZTA4'

dp = Dispatcher()
user_router = Router()

bot = Bot(token=API_TOKEN, parse_mode='HTML')


# @user_router.message(Command('ver1'))
# async def ver1(msg: types.Message) -> None:
#     """Process the 'start' command"""
#     kb = [
#         [types.KeyboardButton(text="GPT")],
#         [types.KeyboardButton(text="SBER")],
#         [types.KeyboardButton(text="YANDEX")],
#     ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
#     await msg.answer('Hello, <b>World</b>!', reply_markup=keyboard)
#
#
@user_router.message(Command('ver2'))
async def main_menu(msg: Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text='Model',
        callback_data='select_model')
    )
    builder.row(InlineKeyboardButton(
        text='Options',
        callback_data='options')
    )
    builder.row(InlineKeyboardButton(
        text='Start a dialogue',
        callback_data='start_use')
    )
    await msg.answer(
        '========  Выберите пункт меню:  =========',
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == 'start_use')
async def start_use(callback: CallbackQuery):
    text = ('Тут мы делаем запрос к модели. \n'
            'Получаем какое-то приветствие и выдаем его пользователю.')
    await bot.answer_callback_query(callback.id)
    await callback.message.answer(text=text)


@dp.callback_query(F.data == 'select_model')
async def select_chat_model(callback: CallbackQuery) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='GPT',
        callback_data='select_model_GPT')
    )
    builder.add(InlineKeyboardButton(
        text='SBER',
        callback_data='select_model_SBER')
    )
    builder.add(InlineKeyboardButton(
        text='YANDEX',
        callback_data='select_model_YANDEX')
    )
    # await msg.answer(
    #     'Выберите модель для дальнейшего диалога:',
    #     reply_markup=builder.as_markup()
    # )
    await bot.answer_callback_query(callback.id)  # Ответ на запрос, чтобы убрать "часики" в кнопке
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        # reply_markup=None)  # Очищаем кнопки
                                        reply_markup=builder.as_markup())  # Заменяем кнопки


@dp.callback_query(F.data == 'select_model_GPT')
async def select_model_gpt(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='GPT 3.5 4k',
        callback_data='select_model_GPT_3_5_4k')
    )
    builder.add(InlineKeyboardButton(
        text='GPT 4 16k',
        callback_data='select_model_GPT_4_0_16k')
    )
    builder.row(InlineKeyboardButton(
        text='<- BACK',
        callback_data='select_model')
    )
    await bot.answer_callback_query(callback.id)  # Ответ на запрос, чтобы убрать "часики" в кнопке
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        # reply_markup=None)  # Очищаем кнопки
                                        reply_markup=builder.as_markup())  # Заменяем кнопки


@dp.callback_query(F.data == 'select_model_SBER')
async def select_model_sber(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="SBER version 1",
        callback_data="select_model_SBER_v1")
    )
    builder.add(types.InlineKeyboardButton(
        text="SBER version 2",
        callback_data="select_model_SBER_v2")
    )
    builder.row(InlineKeyboardButton(
        text='<- BACK',
        callback_data='select_model')
    )
    await bot.answer_callback_query(callback.id)  # Ответ на запрос, чтобы убрать "часики" в кнопке
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        # reply_markup=None)  # Очищаем кнопки
                                        reply_markup=builder.as_markup())  # Заменяем кнопки


@dp.callback_query(F.data == "select_model_GPT_3_5_4k")
async def select_model_gpt_3_5_4k(callback: CallbackQuery):
    text = ('Вы выбрали модель GPT 3.5 4k и мы это помним.\n'
            'Тут можно добавить описание.\n'
            'Или не добавить.')
    await bot.answer_callback_query(callback.id)
    await callback.message.answer(text=text)
    await main_menu(callback.message)


# Обработка любого текстового сообщения от пользователя
@dp.message(F.text)
# async def free_mode(callback: CallbackQuery):
async def free_mode(msg: Message):
    text = ('Мы получили произвольный вопрос от пользователя.\n'
            f'Вот он: <b>{msg.text}</b>\n'
            'Обрабатываем, отвечаем: "бла-бла-бла"')
    # await bot.answer_callback_query(callback.id)
    await msg.answer(text=text)


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(user_router)


async def main() -> None:
    # bot = Bot(token=API_TOKEN, parse_mode='HTML')
    register_routers(dp)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
