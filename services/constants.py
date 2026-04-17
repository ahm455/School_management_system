from django.db import models
from django.utils.translation import gettext_lazy as _

class AttentanceChoices(models.TextChoices):
    PRESENT = "PRES", _("Present")
    ABSENT = "ABS", _("Absent")


class ResultChoices(models.TextChoices):
    PASS = "PASS", _("Pass")
    FAIL = "FAIL", _("Fail")

class SemesterChoices(models.TextChoices):
    FIRST = "FIRST", _("First Semester")
    SECOND = "SECOND", _("Second Semester")


class StatusChoices(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    SUBMITTED= "SUBMITTED", _("Submitted")

class NotificationChoices(models.TextChoices):
    Result = "Result", _("Result")
    Attendance= "Attendance", _("Attendance")
    Assignment = "Assignment", _("Assignment")