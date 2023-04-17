from rest_framework import serializers
from accounts.models import Member
from django.contrib.auth.hashers import make_password


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop("password")
        hashed_password = make_password(password)
        member = Member.objects.create(
            password=hashed_password,
            **validated_data,
        )
        return member


class MemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "firstname",
            "lastname",
            "fullname",
        ]

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
