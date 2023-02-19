from django.contrib.auth.models import User, Group
from car.models import Car, CarDetail, CarMain
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CarMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMain
        fields = ["id", "make", "model"]

class CarDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDetail
        fields = [field.name for field in CarDetail._meta.get_fields()]



class CarSerializer(serializers.ModelSerializer):
    main = CarMainSerializer(read_only=True)
    detail = CarDetailSerializer(read_only=True)
    class Meta:
        model = Car
        fields = ['id','main', 'detail']
