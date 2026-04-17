from rest_framework import serializers
from accounts.models import User, Student, Teacher, Headmaster


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','clerk_id','first_name','last_name','full_name',
                  'email','phone_number','is_headmaster','is_teacher','is_student','date_joined','date_of_birth']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class HeadmasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headmaster
        fields = '__all__'