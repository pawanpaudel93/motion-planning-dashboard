from rest_framework import serializers
from .models import *


class SessionSerializer(serializers.ModelSerializer):
     class Meta:
          model = Session
          fields = "__all__"


class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = ["value"]


class GlobalPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalPosition
        fields = ["value"]


class GlobalHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalHome
        fields = ["value"]


class LocalPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalPosition
        fields = ["value"]


class LocalVelocitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalVelocity
        fields = ["value"]
