import requests


class SendlerMessage:

    def __init__(self, login, passwd):
        self.login = login
        self.passwd = passwd
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/107.0.0.0 '
                          'Safari/537.36',
            'login': self.login,
            'password': self.passwd
        }
        self.headers = headers

        self.list_id = []

    def send(self, phone, text):

        phone = self.check_phone(phone)
        url = f'https://api.iqsms.ru/messages/v2/send/?phone=%2B{phone}&text={text}&login={self.login}&password={self.passwd}'
        response = requests.get(url, headers=self.headers)
        try:
            id = response.split(';')[1]
            if id[0] == 'accepted':
                self.list_id.append(id)
            else:
                return response.text
        except Exception as _err:
            print(f'ошибка отправки сообщения {_err}')
            return response.text
        return response.text

    def status(self, id):
        url = f'https://api.iqsms.ru/messages/v2/status/?id={id}&login={self.login}&password={self.passwd}'
        response = requests.get(url, headers=self.headers)
        return response.text

    def check_phone(self, phone):
        phone = ''.join(filter(str.isdigit, phone))
        if str(phone[0]) != '7':
            phone = phone.replace(phone[0], '7', 1)
            return phone
        else:
            return phone


if __name__ == "__main__":

    phones = {
        'phone': '+79024356567',
        'phone1': '79024356567',
        'phone2': '+89024356567',
        'phone3': '89024356567',
        'phone4': '+7(999)-999-99-99'
    }
    for phone, number in phones.items():
        newTel = ''.join(filter(str.isdigit, number))
        if str(newTel[0]) != '7':
            newTel = newTel.replace(newTel[0], '7', 1)

            print(newTel)
        else:
            print(newTel)
