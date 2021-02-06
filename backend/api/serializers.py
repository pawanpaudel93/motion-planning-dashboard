from rest_framework import serializers
from .models import *


class SessionSerializer(serializers.ModelSerializer):
     class Meta:
          model = Session
          fields = "__all__"


class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = "__all__"


class GlobalPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalPosition
        fields = "__all__"


class GlobalHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalHome
        fields = "__all__"


class LocalPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalPosition
        fields = "__all__"


class LocalVelocitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalVelocity
        fields = "__all__"
