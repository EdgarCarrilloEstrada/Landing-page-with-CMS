from wagtail.admin.viewsets.model import ModelViewSet
from .models import ServiceRequest

# Create your views here.
class ServiceTrackingViewSet(ModelViewSet):
    model = ServiceRequest

    add_to_admin_menu = True
    menu_label = "Seguimiento de servicios"
    menu_name = "Seguimiento de servicios"


    # form_fields = ["client_name", "service_type", "service_description"]
    exclude_form_fields = ["created_at", "updated_at"]
    icon = "history"


    copy_view_enabled = False
    inspect_view_enabled = True


service_tracking_viewset = ServiceTrackingViewSet("service_tracking")