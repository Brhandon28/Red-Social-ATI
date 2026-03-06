from django.conf import settings
from django.db import models
from django.db.models import Q, F


class ConnectionRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        ACCEPTED = 'accepted', 'Aceptada'
        REJECTED = 'rejected', 'Rechazada'

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_connection_requests',
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_connection_requests',
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['sender', 'receiver'], name='unique_connection_request'),
            models.CheckConstraint(condition=~Q(sender=F('receiver')), name='prevent_self_connection_request'),
        ]

    def __str__(self):
        return f'{self.sender} -> {self.receiver} ({self.status})'
