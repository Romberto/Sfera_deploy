from django.core.exceptions import ValidationError
from django.db import models
import bcrypt


def passwd_hash(passwd):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd.encode('utf-8'), salt=salt)
    return hashed, salt

def admin_driver_validator(admin):
    driver = DriverModel.objects.get(login=admin)
    if not driver.admin_bool:
        raise ValidationError('admin must be admin_bool is True')



# Водитель-Экскурсовод
class DriverModel(models.Model):
    driver_name = models.CharField(max_length=50)  # имя
    driver_last_name = models.CharField(max_length=50)  # фамилия
    phone = models.CharField(max_length=50)  # телефон
    login = models.CharField(max_length=30)  # логин
    password = models.CharField(max_length=200, null=True)  # пароль
    salt = models.BinaryField(null=True)  # соль
    password_hash = models.BinaryField(null=True)  # хеш пароля
    admin_bool = models.BooleanField(default=False) # администратор группы
    bot_user_id = models.CharField(max_length=20,null=True, blank=True)  # id юзера для проверки регистрации ботом
    drivers_group = models.ForeignKey('DriverAdminGroupModel', on_delete=models.CASCADE, blank=True, null=True) #группа водителей
    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self):
        return str(self.login)

    def save(self, *args, **kwargs):
        password, salt = passwd_hash(self.password)
        self.password = None
        self.password_hash = password
        self.salt = salt
        super(DriverModel, self).save(*args, **kwargs)

class DriverAdminGroupModel(models.Model):
    name_group = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    admin = models.ForeignKey(DriverModel, on_delete=models.CASCADE, related_name='driver')

    def save(self, **kwargs):
        self.slug = f'{self.name_group}, {self.admin}'
        super(DriverAdminGroupModel, self).save(**kwargs)

    def clean(self):
        driver = DriverModel.objects.get(login=self.admin)
        if not driver.admin_bool:
            raise ValidationError(
                {'admin': "admin must be admin_bool is True"})

    def __str__(self):
        return self.name_group

