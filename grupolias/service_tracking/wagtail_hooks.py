from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from .views import (
    service_tracking_viewset,
    service_dashboard,
)


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
            service_dashboard,
            name="service_dashboard",
        ),
    ]


# ======================================
# DASHBOARD MENU ITEM
# ======================================

@hooks.register("register_admin_menu_item")
def register_service_dashboard_menu_item():
    return MenuItem(
        "Dashboard",
        reverse("service_dashboard"),
        icon_name="tasks",
        order=200,
    )