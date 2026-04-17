from django.contrib import admin
from .models import  *

admin.site.register(Course)
admin.site.register(StudentEnrollment)
admin.site.register(Assignment)
admin.site.register(Submission)
