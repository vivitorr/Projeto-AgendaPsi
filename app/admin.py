from django.contrib import admin
from .models import Events, Notificacoes

def get_all_events():
    events = Events.objects.all()
    return events

@admin.register(Notificacoes)
class NotificacoesAdmin(admin.ModelAdmin):
    pass

def get_all_notificacoes():
    notificacoes = Notificacoes.objects.all()
    return notificacoes