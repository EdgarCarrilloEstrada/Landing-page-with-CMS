from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from .views import (
    service_tracking_viewset,
    service_dashboard,
)

from django.contrib.auth.decorators import permission_required


# ======================================
# CRUD ADMIN
# ======================================

@hooks.register("register_admin_viewset")
def register_viewset():
    return service_tracking_viewset


# ======================================
# DASHBOARD URL
# ======================================

@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path(
            "service-dashboard/",
            permission_required(
                "service_tracking.view_dashboard",
                raise_exception=True
            )(service_dashboard),
            name="service_dashboard",
        ),
    ]


# ======================================
# CUSTOM MENU ITEM
# ======================================

class DashboardMenuItem(MenuItem):

    def is_shown(self, request):

        return request.user.has_perm(
            "service_tracking.view_dashboard"
        )


# ======================================
# DASHBOARD MENU ITEM
# ======================================

@hooks.register("register_admin_menu_item")
def register_service_dashboard_menu_item():

    return DashboardMenuItem(
        "Dashboard",
        reverse("service_dashboard"),
        icon_name="tasks",
        order=801,
    )