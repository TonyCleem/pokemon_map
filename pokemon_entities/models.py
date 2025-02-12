from django.db import models  # noqa F401
from django.db.models import ForeignKey


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name = 'Название')
    title_en = models.CharField(max_length=200, blank=True, verbose_name = 'Название (en)')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name = 'Название (jp)')
    photo = models.ImageField(null=True, verbose_name = 'Изображение')
    description = models.TextField(blank=True, verbose_name = 'Описание')
    previous_evolution = models.ForeignKey("self",
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           related_name='next_evolution',
                                           verbose_name='Предыдущая эволюция'
                                           )


    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                related_name ='entity',
                                verbose_name='Покемон'
                                )
    lat = models.FloatField(null=True, verbose_name = 'Широта')
    lon = models.FloatField(null=True, verbose_name = 'Долгота')
    appeared_at = models.DateTimeField(null=True, verbose_name = 'Дата появления')
    disappeared_at = models.DateTimeField(null=True, verbose_name = 'Дата исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name = 'Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name = 'Здоровье')
    defence = models.IntegerField(null=True, blank=True, verbose_name = 'Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name = 'Выносливость')


    def __str__(self):
        return (f"""Lat: {self.lat}, Lon: {self.lon},
                f'Apeared_at: {self.appeared_at}, Disappeared_at: {self.disappeared_at},
                f'Level: {self.level} , Health: {self.health}, Defence: {self.defence}, Stamina: {self.stamina}""")