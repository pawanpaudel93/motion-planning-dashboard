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


class DroneDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DroneData
        fields = "__all__"


class GlobalPositionSerializer(serializers.ModelSerializer):
    value = serializers.ListField(read_only=True, source="global_position")
    class Meta:
        model = DroneData
        fields = ['timestamp', 'value']


class GlobalHomeSerializer(serializers.ModelSerializer):
    value = serializers.ListField(read_only=True, source="global_home")
    class Meta:
        model = DroneData
        fields = ['timestamp', 'value']


class LocalPositionSerializer(serializers.ModelSerializer):
    value = serializers.ListField(read_only=True, source="local_position")
    class Meta:
        model = DroneData
        fields = ['timestamp', 'value']


class LocalVelocitySerializer(serializers.ModelSerializer):
    value = serializers.ListField(read_only=True, source="local_velocity")
    class Meta:
        model = DroneData
        fields = ['timestamp', 'value']
