from aiogram.utils import executor
from loader import dp
from handlers import auth_client, active_token, report_admin

auth_client.register_handlers_auth(dp)
active_token.register_handlers_token(dp)
report_admin.register_handlers_admin_report(dp)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
