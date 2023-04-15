from rest_framework import serializers
from accounts.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"

    def create(self, validated_data):
        member = Member.objects.create(**validated_data)
        member.save()
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
