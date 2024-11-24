from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from collections import OrderedDict

class BillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bill

        fields = "__all__"
        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields


class OperatSerializer(serializers.ModelSerializer):
    bills = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField()
    bills_count = serializers.SerializerMethodField()

    def get_owner(self, operat):
        return operat.owner.username
    
    def get_moderator(self, operat):
        if operat.moderator:
            return operat.moderator.username
            
    def get_manager(self, operat):
        if operat.manager:
            return operat.manager.username

    def get_bills(self, operat):
        items = BillOperat.objects.filter(operat=operat)
        serializer = BillSerializer([item.bill for item in items], many=True)
        return serializer.data
    
    def get_bills_count(self, operat):
        return BillOperat.objects.filter(operat=operat).count()

    class Meta:
        model = Operat
        fields = '__all__'

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 



class BillOperatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillOperat
        fields = "__all__"

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'date_joined', 'password', 'username')

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)