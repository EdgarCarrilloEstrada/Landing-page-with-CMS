from django.db import models

class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    PAID = "paid", "Pagado"
    PARTIAL = "partial", "Parcial"
    LATE = "late", "Retrasado"
    CANCELLED = "cancelled", "Cancelado"
    REFUNDED = "refunded", "Reembolsado"