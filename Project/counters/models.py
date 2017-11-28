from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Accounts(models.Model):
    id = models.BigIntegerField(primary_key=True, verbose_name='Лицевой счет')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Дом')
    apartments_number = models.CharField(max_length=10, blank=True, null=True, verbose_name='Квартира')
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Лицевой счет'
        verbose_name_plural = 'Лицевые счета'
"""
    @receiver(post_save, sender=User)
    def create_user(sender, instance, created, **kwargs):
        if created and instance.id != 1:
            Accounts.objects.create(user=instance, id=instance.username)

    @receiver(post_save, sender=User)
    def save_user(sender, instance, **kwargs):
        if instance.id != 1:
            instance.accounts.save()

    def __str__(self):
        return str(self.user)"""


class Counters(models.Model):
    id = models.AutoField(primary_key=True)
    id_out_system = models.CharField(blank=True, max_length=8, null=True, unique=True)
    creation_date = models.DateField(blank=True, verbose_name='Дата производства', null=True)
    setup_date = models.DateField(blank=True, verbose_name='Дата установки', null=True)
    in_work = models.BooleanField(default=True, verbose_name='Установлен')
    counter_type = models.CharField(verbose_name='Тип счетчика', max_length=30)
    serial_number = models.CharField(verbose_name='Серийный номер', blank=True, null=True, max_length=10)
    counter_data_simple = models.DecimalField(blank=True, verbose_name='Показания обычные', null=True,
                                              max_digits=9,
                                              decimal_places=3)
    counter_data_day = models.DecimalField(blank=True, verbose_name='Показания день', null=True,
                                           max_digits=9,
                                           decimal_places=3)
    counter_data_night = models.DecimalField(blank=True, verbose_name='Показания ночь', null=True,
                                             max_digits=9,
                                             decimal_places=3)
    old_counter_data_simple = models.DecimalField(blank=True, verbose_name='Прошлый период обычные', null=True,
                                                  max_digits=9,
                                                  decimal_places=3)
    old_counter_data_day = models.DecimalField(blank=True, verbose_name='Прошлый период день', null=True,
                                               max_digits=9,
                                               decimal_places=3)
    old_counter_data_night = models.DecimalField(blank=True, verbose_name='Прошлый период ночь', null=True,
                                                 max_digits=9,
                                                 decimal_places=3)
    date_update = models.DateField(blank=True, null=True, verbose_name='Дата показаний')
    account_id = models.ForeignKey(Accounts, verbose_name='Лицевой счет', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Счетчик'
        verbose_name_plural = 'Счетчики'

    def __str__(self):
        return self.counter_type


class DataHistory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    account_id = models.ForeignKey(Accounts, verbose_name='Лицевой счет', on_delete=models.CASCADE)
    counter_id = models.ForeignKey(Counters, verbose_name='ID Электросчетика', null=True, on_delete=models.CASCADE)
    counter_type = models.CharField(verbose_name='Тип счетчика', max_length=30)
    serial_number = models.CharField(verbose_name='Серийный номер', blank=True, null=True, max_length=10)
    date = models.DateField(blank=True, null=True, verbose_name='Дата показаний')
    data_simple = models.DecimalField(blank=True, verbose_name='Данные счетчика', null=True,
                                      max_digits=9,
                                      decimal_places=3)
    data_day = models.DecimalField(blank=True, verbose_name='Данные по днивному тарифу', null=True,
                                   max_digits=9,
                                   decimal_places=3)
    data_night = models.DecimalField(blank=True, verbose_name='Данные по ночному тарифу', null=True,
                                     max_digits=9,
                                     decimal_places=3)
    in_work = models.BooleanField(default=True, verbose_name='Установлен')

    class Meta:
        verbose_name = 'Счетчик'
        verbose_name_plural = 'Счетчики'

    def __str__(self):
        return self.counter_type
