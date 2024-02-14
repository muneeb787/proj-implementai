from django.db import models
from django.contrib.auth.models import User

class Lead(models.Model):
  class LeadStatuses(models.TextChoices):
    ACTIVE = "AC", "Active"
    PENDING = "PD", "Pending"

  name = models.CharField(max_length=100)
  phone_number = models.CharField(max_length=300)
  vapi_call_id = models.CharField(max_length=100, null=True, blank=True)

  status = models.CharField(
    max_length=2,
    choices=LeadStatuses.choices,
    editable=False,
    default=LeadStatuses.PENDING,
  )
#   created_by = models.ForeignKey(
#     User,
#     on_delete=models.DO_NOTHING,
#     related_name="owned_organization",
#     null=True,
#   )
  created_on = models.DateField(auto_now_add=True)

