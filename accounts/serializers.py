from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','first_name','last_name','full_name','email','phone_number','is_student','is_teacher','is_headmaster','semester','date_joined','date_of_birth','education']