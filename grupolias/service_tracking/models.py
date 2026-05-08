from django.db import models

from shared.enums.services import Services
from shared.enums.states import States
from shared.enums.payment_status import PaymentStatus

# Create your models here.

class ServiceRequest(models.Model):

    # Información general
    client_name = models.CharField(max_length=255, verbose_name="Nombre del cliente")
    service_type = models.CharField(max_length=50, choices=Services.choices, verbose_name="Tipo de servicio")
    service_description = models.TextField(verbose_name="Tema a realizar o resolver")

    # Personal involucrado
    technician_name = models.CharField(max_length=255, verbose_name="Nombre del técnico")
    operator_responsible = models.CharField(max_length=255, verbose_name="Responsable del seguimiento")
    assigned_by = models.CharField(max_length=255, verbose_name="Asignado por")  # arquitecto o ingeniero

    # Fechas y horas
    request_datetime = models.DateTimeField(verbose_name="Fecha y hora de solicitud")

    execution_date = models.DateField(null=True, verbose_name="Fecha de realización")
    completion_date = models.DateField(null=True, verbose_name="Fecha de termino")

    payment_date = models.DateField(null=True, verbose_name="Fecha de pago")

    # Ubicación
    place_name = models.CharField(max_length=255, verbose_name="Nombre del lugar")
    place_manager_name = models.CharField(max_length=255, verbose_name="Nombre del encargado del lugar")
    address = models.TextField(verbose_name="Dirección")
    state = models.CharField(max_length=5, choices=States.choices, verbose_name="Estado")

    # Resultados del servicio
    work_description = models.TextField(verbose_name="Descripción de lo que se realizó")

    # Costos
    technician_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo del técnico")
    company_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de Grupo LIAS")

    # Pago
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, verbose_name="Estado del pago")

    # Extras
    general_observations = models.TextField(blank=True, verbose_name="Observaciones")

    # Control interno
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.client_name} - {self.service_type} - {self.request_date}"