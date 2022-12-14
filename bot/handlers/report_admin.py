from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from database.config_db import check_auth
from database.token_db import check_driver_admin, make_lxml, answer_all_sales
from keyboard.driver_kb import kb_drivers
from states import ReportState, ActivateTokenState


async def choice_report(call: types.CallbackQuery, state=FSMContext):
    login_auth = await check_auth(str(call.message.chat.id))
    if call.data == 'my':
        buf = await make_lxml(str(login_auth.id), login_auth.login)
        if buf:
            await call.message.answer(buf[1], reply_markup=kb_drivers)
            await call.message.answer_document(document=buf[0])

        else:
            await call.message.answer(f'Логин {login_auth.login}\n** Сегодня продаж небыло', reply_markup=kb_drivers)

        await ActivateTokenState.start.set()
    elif call.data == 'all':

        data = await state.get_data()
        id_group =data['group_id']
        buf = await answer_all_sales(id_group)
        if buf:
            await call.message.answer(buf[1], reply_markup=kb_drivers)
            await call.message.answer_document(buf[0])
            await ActivateTokenState.start.set()
        else:
            await call.message.answer(f'Логин {login_auth.login}\n** Сегодня продаж небыло', reply_markup=kb_drivers)
    elif call.data == 'back':
        await state.finish()
        await call.message.answer("С помощью кнопки 'проверить код', активируйте жетон", reply_markup=kb_drivers)
        await ActivateTokenState.start.set()
        await state.update_data(driver_id=login_auth.id)

async def choice_report_text(message: types.Message, state=FSMContext,):
    if message.text == 'Проверить код':
        await ActivateTokenState.next()
        await message.answer('Отправте жетон')
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
            await message.answer('Выберайте отчёт', reply_markup=kb_admin)
            await ReportState.start.set()
            await state.update_data(driver_id=is_adm['id'])
            await state.update_data(group_id=is_adm['drivers_group'])
        else:
            buf = await make_lxml(str(is_adm['id']), is_adm['login'])
            await message.answer(buf[1], reply_markup=kb_drivers)
            await message.answer_document(document=buf[0])
            await ActivateTokenState.start.set()
    else:
        await message.answer('текстовые сообщения недопустимы')



def register_handlers_admin_report(dp: Dispatcher):
    dp.register_callback_query_handler(choice_report, state=ReportState.start)
    dp.register_message_handler(choice_report_text,state=ReportState.start, content_types=['text'])