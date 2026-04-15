from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','clerk_id','first_name','last_name','full_name',
                  'email','phone_number','is_headmaster','is_teacher','is_student','semester','date_joined','date_of_birth']

    def validate(self, data):
        roles = [
            data.get("is_student", False),
            data.get("is_teacher", False),
            data.get("is_headmaster", False),]

        if sum(roles) > 1:
            raise serializers.ValidationError("Only one role can be true at a time.")

        return data
