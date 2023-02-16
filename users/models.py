from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import check_birth_date, check_email_address


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class User(AbstractUser):
    CHOICES = [('member', 'участник'), ('moderator', 'модератор'), ('admin', 'администратор')]

    role = models.CharField(choices=CHOICES, max_length=9, default='member')
    age = models.PositiveSmallIntegerField(null=True)
    location = models.ManyToManyField(Location)
    birth_date = models.DateField(verbose_name='Дата рождения', validators=[check_birth_date], blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True, validators=[check_email_address])

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

