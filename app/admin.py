from django.contrib import admin
from .models import Events

def get_all_events():
    events = Events.objects.all()
    return events

admin.site.register(Events)