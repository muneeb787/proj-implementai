from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
  class OrganizationStatuses(models.TextChoices):
    ACTIVE = "AC", "Active"

  owner = models.ForeignKey(
    User,
    on_delete=models.DO_NOTHING,
    related_name="owned_organization",
    null=True,
  )
  name = models.CharField(max_length=300, null=True)
  status = models.CharField(
    max_length=2,
    choices=OrganizationStatuses.choices,
    editable=False,
    default=OrganizationStatuses.ACTIVE,
  )
  created_on = models.DateField(auto_now_add=True)