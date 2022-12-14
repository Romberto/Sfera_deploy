from aiogram import types, Dispatcher
import bcrypt
from database.config_db import get_user_db, check_auth, add_user
from aiogram.dispatcher import FSMContext
from keyboard.driver_kb import kb_drivers
from states import AuthState, ActivateTokenState


async def echo(message: types.Message, state=FSMContext):
    await state.finish()
    login_auth = await check_auth(str(message.from_user.id))
    if not login_auth:
        await message.answer('Добрый день для регистрации введите Логин:')
        await AuthState.login.set()

    else:
        await message.answer("С помощью кнопки 'проверить код', активируйте экскурсию", reply_markup=kb_drivers)
        await ActivateTokenState.start.set()
        await state.update_data(driver_id=login_auth.id)


# обработчик сообщения с логином
async def get_login(message: types.Message, state=FSMContext):
    login_text = message.text
    user = await get_user_db(login_text)
    if user:
        await AuthState.next()
        await message.answer('Отлично ' + user.driver_name + ', теперь пароль:')
        await state.update_data(login=login_text)
    else:
        await message.answer('Извените, пользователя с таким логином не найдено.')


#    обработчик собщения с паролем
async def get_passwd(message: types.Message, state=FSMContext):
    passwd_cheked = message.text
    state_data = await state.get_data()
    login = state_data['login']
    driver = await get_user_db(login)
    hashed_passwd = bcrypt.hashpw(passwd_cheked.encode('utf-8'), driver.salt.tobytes())
    if hashed_passwd == driver.password_hash.tobytes():
        await add_user(str(message.from_user.id), driver.id)
        await state.finish()
        await message.answer("С помощью кнопки 'проверить код', активируйте жетон", reply_markup=kb_drivers)
        await ActivateTokenState.start.set()
    else:
        await message.answer('Извените, но пароль не подошёл, попробуйте ещё разок.')


def register_handlers_auth(dp: Dispatcher):
    dp.register_message_handler(echo, commands=['start'], state='*')
    dp.register_message_handler(get_login, state=AuthState.login, content_types=['text'])
    dp.register_message_handler(get_passwd, state=AuthState.passwd, content_types=['text'])
