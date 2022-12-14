from random import randint

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from excursions.models import ExcursionModel, ExcursionPhoneCodModel, ExcursionPointModel
from sendler import SendlerMessage
from tokens.models import TokenExModel


class ExcursionsView(View):
    def get(self, request):
        excursions = ExcursionModel.objects.all()
        return render(request, 'excursions/excursions.html', {
            'excursions': excursions
        })


# Экскурсия return экскурсия по id
class ExcursionItemView(View):

    def get(self, request, id):
        excursion = ExcursionModel.objects.get(id=id)
        return render(request, 'excursions/excur_item.html', {
            'excursion': excursion
        })


class GalleryView(View):

    def get(self, request):
        points = ExcursionPointModel.objects.all()  # все точки экскурсий
        return render(request, 'excursions/excur_gallery.html', {
            'range': [1, 2, 3, 4, 5],
            'points': points
        })


class PointGalleryView(View):
    def get(self, request, id):
        point = ExcursionPointModel.objects.get(id=id)
        excursions = ExcursionModel.objects.filter(point__name=point.name)
        count = len(excursions)
        return render(request, 'excursions/point_gallery.html', {
            'point': point,
            'excursions': excursions,
            'count': count
        })


# генерация кода для подтверждения телефона
def checkPhone(request):
    id_excursion = request.GET.get('id')
    phone = request.GET.get('phone')
    excursion_db = ExcursionModel.objects.get(id=id_excursion)
    body = randint(1111, 9999)  # код для сверки телефона
    code = ExcursionPhoneCodModel.objects.filter(phone=phone)
    if code:
        code[0].random_cod = body
        code[0].save()
    else:
        code = ExcursionPhoneCodModel(
            phone=phone,
            random_cod=body,
            excursions=excursion_db
        )
        code.save()
    data = {
        "code": body,
        "status": 200,
        "phone": phone
    }
    #sendler = SendlerMessage()

    #sendler.send(phone, body)

    # todo срабатывает функция, которая отправляет СМС с кодом на номер {phone} код {body}
    print(f'срабатывает функция, которая отправляет СМС с кодом на номер {phone} код {body}')
    return JsonResponse(data)


def checkCode(request):
    code_input = request.GET.get('code')
    phone = request.GET.get('phone')
    status = True
    try:
        code = ExcursionPhoneCodModel.objects.get(phone=phone)
        if not str(code.random_cod) == code_input:
            status = False
            phone = phone

    except Exception as _err:
        print('*******', _err)
        phone = None
        status = False

    data = {
        'code': status,
        'phone': phone
    }
    return JsonResponse(data)



def ExcCod(request):
    exc = request.GET.get('exc')
    phone = request.GET.get('phone')
    excursion = ExcursionModel.objects.get(name=exc)
    body = randint(11111, 99999)
    #sendler = SendlerMessage()
    #phone = sendler.check_phone(phone)
    token = TokenExModel(
        body = body,
        phone = phone,
        excursion = excursion
    )
    token.save()


    #sendler.send(phone, body)


    data={
        'exc': exc,
        'phone': phone,
        'body': body
    }
    return JsonResponse(data)
