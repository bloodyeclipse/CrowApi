from rest_framework import serializers
from django.contrib.auth.models import Group
from django.conf import settings

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    user_group = serializers.CharField(style={'input_type': 'text'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'user_group', 'first_name', 'last_name', 'profile_img',
                  'uid']
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_img': {'read_only': True},
            'uid': {'read_only': True}
        }

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value
    def save(self):
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': "Passwords must match"})
        account.set_password(password)

        submitted_group = self.validated_data['user_group'].lower()
        print(submitted_group)
        group = Group.objects.get(name=submitted_group)
        if group.name == "admin":
            account.is_admin = True
            account.is_staff = True
        if group.name == "manager":
            account.is_staff = True
        if group.name == "driver":
            account.is_staff = False
        account.save()
        account.groups.add(group)
        return account
