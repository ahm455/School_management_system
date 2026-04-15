from django.db import models
from django.utils.translation import gettext_lazy as _

class AttentanceChoices(models.TextChoices):
    PRESENT = "PRES", _("Present")
    ABSENT = "ABS", _("Absent")


class ResultChoices(models.TextChoices):
    PASS = "PASS", _("Pass")
    FAIL = "FAIL", _("Fail")

class SemesterChoices(models.IntegerChoices):
    FIRST = "1", _("1")
    SECOND = "2", _("2")


class StatusChoices(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    SUBMITTED= "SUBMITTED", _("Submitted")