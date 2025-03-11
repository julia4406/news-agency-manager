from django.db import models


class TaskStatuses(models.TextChoices):
    DONE = "Done", "Done"
    ASSIGNED = "Assigned", "Assigned"
    OVERDUE = "Overdue", "Overdue"