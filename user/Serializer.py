from rest_framework import serializers
from django.contrib.auth.models import Group

from .models import User



class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    user_group = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'user_group', 'first_name', 'last_name','profile_img','uid']
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_img': {'read_only':True},
            'uid': {'read_only':True}
        }

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
        group = Group.objects.get(name=submitted_group)
        if group.name == "Admin":
            account.is_admin = True
            account.is_staff = True
        if group.name == "Manager":
            account.is_staff = True
        if group.name == "Driver":
            account.is_staff = False
        account.save()
        account.groups.add(group)

        if group.name == "Manager":
            self.set_teacher(account)
        # Create OLAP is user is a learner
        # if group.name == "learner":
        #     # get OLAP
        return account