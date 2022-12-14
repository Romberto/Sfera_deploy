from aiogram import types, Dispatcher
import bcrypt

from database.token_db import get_token, token_finaly, check_driver_admin, personal_sales, make_lxml
from keyboard.driver_kb import kb_drivers
from keyboard.token_active_kb import kb_tokens
from states import ActivateTokenState, ReportState
from aiogram.dispatcher import FSMContext


# отслеживает нажатие на кнопку Проверить токен или Отчёт за сегодня
async def token_get(message: types.Message, state=FSMContext):
    if message.text == 'Проверить код':
        await ActivateTokenState.next()
        await message.answer('Отправте токен жетон')
    elif message.text == 'Отчёт за сегодня':
        await state.finish()
        is_adm = await check_driver_admin(str(message.from_user.id))
        if is_adm['admin_bool']:
            kb_admin = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
                types.InlineKeyboardButton(text='МОИ ПРОДАЖИ', callback_data='my'),
                types.InlineKeyboardButton(text='ВСЕ ПРОДАЖИ', callback_data='all'),
                types.InlineKeyboardButton(text='НАЗАД', callback_data='back')
            ]
            kb_admin.add(*buttons)
            await message.answer(f'Выберайте отчёт', reply_markup=kb_admin)
            await ReportState.start.set()
            await state.update_data(group_id=is_adm['drivers_group'])
            await state.update_data(driver_id=is_adm['id'])
        else:
            buf = await make_lxml(str(is_adm['id']), is_adm['login'])
            await ActivateTokenState.start.set()
            if buf:
                await message.answer(buf[1], reply_markup=kb_drivers)
                await message.answer_document(document=buf[0])
            else:
                await message.answer(f'Логин {is_adm["login"]}\n** Сегодня продаж небыло')

async def check_token(message: types.Message, state=FSMContext):

    if message.text == 'Проверить код':
        await ActivateTokenState.token.set()
        await message.answer('Отправте код жетона')

    elif message.text == 'Отчёт за сегодня':
        await state.finish()
        is_adm = await check_driver_admin(str(message.from_user.id))
        if is_adm['admin_bool']:
            kb_admin = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton(text='МОИ ПРОДАЖИ', callback_data='my'),
                types.InlineKeyboardButton(text='ВСЕ ПРОДАЖИ', callback_data='all'),
                types.InlineKeyboardButton(text='НАЗАД', callback_data='back')
            ]
            kb_admin.add(*buttons)
            await message.answer('Выберайте отчёт', reply_markup=kb_admin)
            await ReportState.start.set()
            await state.update_data(driver_id=is_adm['id'])
            await state.update_data(group_id=is_adm['drivers_group'])
        else:
            buf = await make_lxml(str(is_adm['id']), is_adm['login'])
            await ActivateTokenState.start.set()
            if buf:
                await message.answer(buf[1], reply_markup=kb_drivers)
                await message.answer_document(document=buf[0])
            else:
                await message.answer(f'Логин {is_adm["login"]}\n** Сегодня продаж небыло')
    else:
        is_adm = await check_driver_admin(str(message.from_user.id))
        token_text = message.text
        token = await get_token(token_text)
        if token:
            await state.update_data(token=token_text)
            await state.update_data(driver_id=is_adm['id'])

            await message.reply('Жетон ' + token.excursion_name + '\nцена: ' + str(token.excursion_price) + '',
                                reply_markup=kb_tokens)
            await ActivateTokenState.next()
        else:
            await message.reply('Активных токенов с таким кодом не найдено\nВведите токен ещё раз или \nотправте /start, чтобы вернуться в меню.')
            await ActivateTokenState.token.set()


async def active_token(message: types.Message, state=FSMContext):
    if message.text == 'Активировать':

        kb_enroll = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(text='ДА', callback_data='yes'),
            types.InlineKeyboardButton(text='НЕТ', callback_data='no')
        ]
        kb_enroll.add(*buttons)
        await message.answer("Активировать, \nВы уверены ? ", reply_markup=kb_enroll)
        await ActivateTokenState.next()
    elif message.text == 'Назад':
        await message.answer("С помощью кнопки 'проверить код', активируйте жетон", reply_markup=kb_drivers)
        await ActivateTokenState.start.set()


async def token_finish(call: types.CallbackQuery, state=FSMContext):
    if call.data == 'yes':
        data = await state.get_data()
        await call.message.answer(f'Активирую')

        token = data['token']
        driver = data['driver_id']
        finale = await token_finaly(token, str(driver))
        if finale:
            await call.message.answer("Успешная активация !\nС помощью кнопки 'проверить код', активируйте экскурсию", reply_markup=kb_drivers)
            await ActivateTokenState.start.set()
        else:
            await call.message.answer("*** Ошибка ***\nПроблемы с активацией !")
    elif call.data == 'no':
        await call.answer('назад', cache_time=3)
        await call.message.answer("С помощью кнопки 'проверить код', активируйте жетон", reply_markup=kb_drivers)
        await ActivateTokenState.start.set()


async def token_error(message: types.Message):
    await message.answer("Извените я не понимаю, если хотите проверить оплату нажмите кнопку 'Проверить код'")


def register_handlers_token(dp: Dispatcher):
    dp.register_message_handler(token_get, state=ActivateTokenState.start, content_types=['text'],
                                text=['Проверить код', 'Отчёт за сегодня'])
    dp.register_message_handler(check_token, state=ActivateTokenState.token, content_types=['text'])
    dp.register_message_handler(active_token, state=ActivateTokenState.token_active, content_types=['text'])
    dp.register_callback_query_handler(token_finish, state=ActivateTokenState.token_finish)
  #  dp.register_message_handler(token_error, content_types=['text'], state='*')
