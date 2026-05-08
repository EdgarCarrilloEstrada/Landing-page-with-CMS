from wagtail import hooks
from .views import service_tracking_viewset

@hooks.register("register_admin_viewset")
def register_viewset():
    return service_tracking_viewset