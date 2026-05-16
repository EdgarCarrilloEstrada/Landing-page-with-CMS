from django.db import models
import uuid

from shared.enums.services import Services
from shared.enums.states import States
from shared.enums.payment_status import PaymentStatus
from shared.enums.service_status import ServiceStatus

from wagtail.images import get_image_model_string
from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.models import ClusterableModel

# Create your models here.


def service_request_image_upload_to(instance, filename):
    return f"service-tracking/{instance.service_request.id}/{uuid.uuid4()}-{filename}"

class ServiceRequest(ClusterableModel):

    # Información general
    client_name = models.CharField(max_length=255, verbose_name="Nombre del cliente")
    service_type = models.CharField(max_length=50, choices=Services.choices, verbose_name="Tipo de servicio")
    service_description = models.TextField(verbose_name="Tema a realizar o resolver")
    service_status = models.CharField(max_length=20, choices=ServiceStatus.choices, default=ServiceStatus.PENDING, verbose_name="Estado del servicio")

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

    panels = [
        MultiFieldPanel(
            [
                FieldPanel(field_name="client_name"),
                FieldPanel(field_name="service_type"),
                FieldPanel(field_name="service_description"),
                FieldPanel(field_name="service_status"),
            ],
            heading="Información general",
        ),
        MultiFieldPanel(
            [
                FieldPanel(field_name="technician_name"),
                FieldPanel(field_name="operator_responsible"),
                FieldPanel(field_name="assigned_by"),
            ],
            heading="Personal involucrado",
        ),
        MultiFieldPanel(
            [
                FieldPanel(field_name="request_datetime"),
                FieldPanel(field_name="execution_date"),
                FieldPanel(field_name="completion_date"),
                FieldPanel(field_name="payment_date"),
            ],
            heading="Fechas y horas",
        ),
        MultiFieldPanel(
            [
                FieldPanel(field_name="place_name"),
                FieldPanel(field_name="place_manager_name"),
                FieldPanel(field_name="address"),
                FieldPanel(field_name="state"),
            ],
            heading="Ubicación",
        ),
        MultiFieldPanel(
            [
                FieldPanel(field_name="work_description"),
            ],
            heading="Resultados del servicio",
        ),
        MultiFieldPanel(
            [
                FieldPanel(field_name="technician_cost"),
                FieldPanel(field_name="company_cost"),
            ],
            heading="Costos",
        ),
        MultiFieldPanel(
            [
                FieldPanel(field_name="payment_status"),
            ],
            heading="Pago",
        ),
        MultiFieldPanel(
            [
                FieldPanel(field_name="general_observations"),
                InlinePanel(
                    "service_result_images",
                    heading="Imágenes del trabajo realizado",
                    label="Imagen",
                    max_num=3
                ),
            ],
            heading="Extras",
        ),
    ]


    def __str__(self):
        return f"{self.client_name} - {self.service_type} - {self.request_datetime}"
    
class ServiceRequestImage(models.Model):
    service_request = ParentalKey(
        "ServiceRequest",
        related_name="service_result_images",
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to=service_request_image_upload_to,
    )