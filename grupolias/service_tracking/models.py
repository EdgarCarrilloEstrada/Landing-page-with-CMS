from django.db import models

from shared.enums.services import Services
from shared.enums.states import States
from shared.enums.payment_status import PaymentStatus

# Create your models here.

class ServiceRequest(models.Model):

    # Información general
    client_name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=50, choices=Services.choices)
    service_description = models.TextField()

    # Personal involucrado
    technician_name = models.CharField(max_length=255)
    operator_responsible = models.CharField(max_length=255)
    assigned_by = models.CharField(max_length=255)  # arquitecto o ingeniero

    # Fechas y horas
    request_date = models.DateField()
    request_time = models.TimeField()

    execution_date = models.DateField(null=True)
    completion_date = models.DateField(null=True)

    payment_date = models.DateField(null=True)

    # Ubicación
    place_name = models.CharField(max_length=255)
    place_manager_name = models.CharField(max_length=255)
    address = models.TextField()
    state = models.CharField(max_length=5, choices=States.choices)

    # Resultados del servicio
    work_description = models.TextField()

    # Costos
    technician_cost = models.DecimalField(max_digits=10, decimal_places=2)
    company_cost = models.DecimalField(max_digits=10, decimal_places=2)

    # Pago
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)

    # Extras
    general_observations = models.TextField(blank=True)

    # Control interno
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_name} - {self.service_type} - {self.request_date}"