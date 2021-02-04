from django.db import models
from django.contrib.postgres.fields import ArrayField


class Session(models.Model):
    target_altitude = models.IntegerField("Taeget Altitide")


class BaseModel(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    value = ArrayField(models.FloatField())

    class Meta:
        abstract = True


class Movement(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    value = ArrayField(models.IntegerField())


class GlobalPosition(BaseModel):
    class Meta:
        verbose_name = _("Global Position")
        verbose_name_plural = _("Global Positions")
        db_table = "global_position"


class GlobalHome(BaseModel):
    class Meta:
        verbose_name = _("Global Home")
        verbose_name_plural = _("Global Home")
        db_table = "global_home"


class LocalPosition(BaseModel):
    class Meta:
        verbose_name = _("Local Position")
        verbose_name_plural = _("Local Positions")
        db_table = "local_position"


class LocalVelocity(BaseModel):
    class Meta:
        verbose_name = _("Local Velocity")
        verbose_name_plural = _("Local Velocities")
        db_table = "local_velocity"
