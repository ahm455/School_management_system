from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Student, Teacher, Headmaster


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            Student.objects.create(user=instance)

        elif instance.is_teacher:
            Teacher.objects.create(user=instance)

        elif instance.is_headmaster:
            Headmaster.objects.create(user=instance)