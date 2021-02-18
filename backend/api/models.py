from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _


class Session(models.Model):
    target_altitude = models.IntegerField("Target Altitude")
    start = ArrayField(models.FloatField(), null=True)
    goal = ArrayField(models.FloatField(), null=True)
    is_finished = models.BooleanField("Is Finished", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = _('Session')
        verbose_name_plural = _('Sessions')
        db_table = "session"


class BaseModel(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    value = ArrayField(models.FloatField())

    class Meta:
        abstract = True


class Movement(BaseModel):
    class Meta:
        get_latest_by = 'id'
        verbose_name = _("Movement")
        verbose_name_plural = _("Movements")
        db_table = "movement"


class GlobalPosition(BaseModel):
    class Meta:
        get_latest_by = 'id'
        verbose_name = _("Global Position")
        verbose_name_plural = _("Global Positions")
        db_table = "global_position"


class GlobalHome(BaseModel):
    class Meta:
        get_latest_by = 'id'
        verbose_name = _("Global Home")
        verbose_name_plural = _("Global Home")
        db_table = "global_home"


class LocalPosition(BaseModel):
    class Meta:
        get_latest_by = 'id'
        verbose_name = _("Local Position")
        verbose_name_plural = _("Local Positions")
        db_table = "local_position"


class LocalVelocity(BaseModel):
    class Meta:
        get_latest_by = 'id'
        verbose_name = _("Local Velocity")
        verbose_name_plural = _("Local Velocities")
        db_table = "local_velocity"
