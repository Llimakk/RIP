from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"


class OperatSerializer(serializers.ModelSerializer):
    bills = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()
    bills_count = serializers.SerializerMethodField()

    # def get_owner(selfself, operat):
    #     return operat.owner

    # def get_moderator(selfself, operat):
    #     if operat.moderator:
    #         return operat.moderator

    def get_owner(self, operat):
        if operat.owner:
            return UserSerializer(operat.owner).data
        return None

    def get_moderator(self, operat):
        if operat.moderator:
            return UserSerializer(operat.moderator).data
        return None
            
    def get_bills(self, operat):
        items = BillOperat.objects.filter(operat=operat)
        serializer = BillSerializer([item.bill for item in items], many=True)
        return serializer.data
    
    def get_bills_count(self, operat):
        return BillOperat.objects.filter(operat=operat).count()

    class Meta:
        model = Operat
        fields = '__all__'


class OperatsSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    # def get_owner(self, operat):
    #     return operat.owner

    # def get_moderator(self, operat):
    #     if operat.moderator:
    #         return operat.moderator

    def get_owner(self, operat):
        if operat.owner:
            return UserSerializer(operat.owner).data
        return None

    def get_moderator(self, operat):
        if operat.moderator:
            return UserSerializer(operat.moderator).data
        return None

    class Meta:
        model = Operat
        fields = "__all__"


class BillOperatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillOperat
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'date_joined', 'password', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

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