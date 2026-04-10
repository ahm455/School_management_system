from django.db import models
from django.utils.translation import gettext_lazy as _

class AttentanceChoices(models.TextChoices):
    PRESENT = "PRES", _("Present")
    ABSENT = "ABS", _("Absent")

class RolesChoices(models.TextChoices):
    TEACHER = "TEACHER", _("Teacher")
    STUDENT= "STUDENT", _("Student")
    HEADMASTER = "HEADMASTER", _("Headmaster")

class ResultChoices(models.TextChoices):
    PASS = "PASS", _("Pass")
    FAIL = "FAIL", _("Fail")

class SemesterChoices(models.TextChoices):
    ONE = "ONE", _("One")
    TWO = "TWO", _("Two")

class EducationChoices(models.TextChoices):
    BACHELORS = "BACHELOR", _("Bachelor")
    MASTERS = "MASTER", _("Master")
    PHD = "PHD", _("Phd")

class StatusChoices(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    SUBMITTED= "SUBMITTED", _("Submitted")