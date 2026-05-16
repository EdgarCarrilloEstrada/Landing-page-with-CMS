from django.db import models

class ServiceStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    ASSIGNED = "assigned", "Asignado"
    IN_PROGRESS = "in_progress", "En proceso"
    COMPLETED = "completed", "Completado"
    CANCELLED = "cancelled", "Cancelado"

