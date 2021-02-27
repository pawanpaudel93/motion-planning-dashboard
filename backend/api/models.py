from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _


class Session(models.Model):
    target_altitude = models.IntegerField("Target Altitude")
    safety_distance = models.IntegerField("Safety Distance", default=5)
    start = ArrayField(models.FloatField(), null=True)
    goal = ArrayField(models.FloatField(), null=True)
    is_finished = models.BooleanField("Is Finished", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Session')
        verbose_name_plural = _('Sessions')
        db_table = "session"


class Movement(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    value = ArrayField(models.FloatField())

    class Meta:
        get_latest_by = 'id'
        verbose_name = _("Movement")
        verbose_name_plural = _("Movements")
        db_table = "movement"

class DroneData(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    local_position = ArrayField(models.FloatField())
    local_velocity = ArrayField(models.FloatField())
    global_position = ArrayField(models.FloatField())
    global_home = ArrayField(models.FloatField())

    class Meta:
        get_latest_by = 'id'
        verbose_name = _("Drone Data")
        verbose_name_plural = _("Drone Datas")
        db_table = "drone_data"