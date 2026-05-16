from wagtail.admin.viewsets.model import ModelViewSet
from .models import ServiceRequest

# Create your views here.
class ServiceTrackingViewSet(ModelViewSet):
    model = ServiceRequest

    add_to_admin_menu = True
    menu_label = "Seguimiento de servicios"
    menu_name = "Seguimiento de servicios"

    exclude_form_fields = ["created_at", "updated_at"]
    icon = "history"

    copy_view_enabled = False
    inspect_view_enabled = True

    list_display = [
        "request_datetime", 
        "service_type_label",
        "service_status_label",
        "state_label", 
        "payment_status_label",
    ]

    list_filter = [
        "request_datetime", 
        "service_type", 
        "service_status",
        "state",
        "payment_status",
        "technician_name",
        "operator_responsible",
        "execution_date",
        "completion_date",
        "payment_date",
    ]


service_tracking_viewset = ServiceTrackingViewSet("service_tracking")