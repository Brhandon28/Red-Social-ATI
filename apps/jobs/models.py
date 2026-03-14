from django.conf import settings
from django.db import models
from django.utils import timezone


class JobOffer(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_offers',
    )
    company_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary_range = models.CharField(max_length=120, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.company_name}'

    @property
    def company(self):
        return self.company_name

    @property
    def summary(self):
        return self.description

    @property
    def age(self):
        delta = timezone.now() - self.created_at
        if delta.days > 0:
            return f'{delta.days} d'
        hours = delta.seconds // 3600
        if hours > 0:
            return f'{hours} h'
        minutes = delta.seconds // 60
        if minutes > 0:
            return f'{minutes} min'
        return 'Ahora'


class JobApplication(models.Model):
    offer = models.ForeignKey(
        JobOffer,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_applications',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['offer', 'applicant'],
                name='unique_job_application_per_user',
            )
        ]

    def __str__(self):
        return f'{self.applicant} -> {self.offer}'
