from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid
"""Here all models"""


def generate_single_referral_code():
    ref = str(uuid.uuid4())[:8]
    return ref


def get_id():
    _id = 191000
    while User.objects.filter(username=str(_id)).exists():
        _id += 1
    return str(_id)


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=6,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    country = models.CharField(max_length=20 , choices=(
        ['bangladesh' , 'Bangladesh (+88)'] ,
        ['india' , 'India (+91)']
    ),default='bangladesh'
    )
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals')
    active_permision = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    balance = models.CharField(max_length=6 , default = 100)
    whatsapp_number = models.CharField(max_length=11)
    referral_code = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = get_id()
        if not self.referral_code:
            self.referral_code = generate_single_referral_code()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

class History(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='history', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    why = models.CharField(max_length=100)
    balance = models.CharField(max_length=7)
    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.why} {self.balance}'


class Refer(models.Model):
    refered_from = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE , related_name='refer_from')
    refered_student = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE , related_name='refer_student')
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['time']
    def __str__(self):
        return self.refered_student.username

class Event(models.Model):
    text = models.CharField(max_length=100)
    def __str__(self):
        return self.text