from django.contrib import admin
from .models import User , History , Refer , Event

admin.site.register(User)
admin.site.register(History)
admin.site.register(Refer)
admin.site.register(Event)