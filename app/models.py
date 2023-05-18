from django.db import models
from django.contrib.auth.models import User as AuthUser


class Events(models.Model):
    criador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='criador', to_field='username')
    nomecriador = models.TextField()
    paciente = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='paciente', to_field='username', related_name='events_paciente_set', blank=True, null=True)
    nomepaciente = models.TextField(blank=True, null=True)
    title = models.TextField()
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'events'