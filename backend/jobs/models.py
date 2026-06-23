from django.conf import settings
from django.db import models

class Application(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_REVIEWED = "REVIEWED"
    STATUS_REJECTED = "REJECTED"
    STATUS_ACCEPTED = "ACCEPTED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_ACCEPTED, "Accepted"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.job} ({self.status})"

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    saved_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='saved_jobs',
        blank=True
    )

    def __str__(self):
        return self.title