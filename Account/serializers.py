from .models import MyUser, Role, Question
from rest_framework import serializers

from .models import SystemAccess


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

    def create(self, validated_data):
        return Role.objects.create(**validated_data)


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

    def create(self, validated_data):
        user = MyUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            role_id=validated_data['role_id'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    # def create(self, validated_data):
    #     return MyUser.objects.create(**validated_data)


class SystemAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAccess
        fields = '__all__'

    def create(self, validated_data):
        return SystemAccess.objects.create(**validated_data)




class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        return Question.objects.create(**validated_data)
