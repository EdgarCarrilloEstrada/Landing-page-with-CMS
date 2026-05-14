import json
import pandas as pd

from django.shortcuts import render
from django.db.models import Count, Sum

from wagtail.admin.viewsets.model import ModelViewSet

from .models import ServiceRequest


# =========================
# VIEWSET ADMIN CRUD
# =========================

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

def service_dashboard(request):

    queryset = ServiceRequest.objects.all()

    total_services = queryset.count()

    completed_services = queryset.exclude(
        completion_date=None
    ).count()

    pending_services = queryset.filter(
        completion_date=None
    ).count()

    total_income = (
        queryset.aggregate(
            total=Sum("company_cost")
        )["total"] or 0
    )

    total_technician_cost = (
        queryset.aggregate(
            total=Sum("technician_cost")
        )["total"] or 0
    )

    estimated_profit = (
        total_income - total_technician_cost
    )

    # =====================================
    # PANDAS DATAFRAME
    # =====================================

    values = queryset.values(
        "id",
        "service_type",
        "technician_name",
        "state",
        "request_datetime",
        "completion_date",
        "company_cost",
        "technician_cost",
    )

    df = pd.DataFrame(list(values))

    monthly_labels = []
    monthly_data = []

    avg_completion_days = 0

    top_technician = "N/A"

    top_state = "N/A"

    if not df.empty:

        # =========================
        # FECHAS
        # =========================

        df["request_datetime"] = pd.to_datetime(
            df["request_datetime"]
        )

        df["completion_date"] = pd.to_datetime(
            df["completion_date"]
        )

        # =========================
        # SERVICIOS POR MES
        # =========================

        monthly = (
            df.groupby(
                df["request_datetime"].dt.strftime("%Y-%m")
            )
            .size()
            .reset_index(name="total")
        )

        monthly_labels = monthly["request_datetime"].tolist()

        monthly_data = monthly["total"].tolist()

        # =========================
        # TIEMPO PROMEDIO
        # =========================

        completed_df = df.dropna(
            subset=["completion_date"]
        ).copy()

        if not completed_df.empty:

            completed_df["days_to_complete"] = (
                completed_df["completion_date"].dt.tz_localize(None)
                - completed_df["request_datetime"].dt.tz_localize(None)
            ).dt.days

            avg_completion_days = round(
                completed_df["days_to_complete"].mean(),
                1
            )

        # =========================
        # TOP TÉCNICO
        # =========================

        tech_series = (
            df["technician_name"]
            .value_counts()
        )

        if not tech_series.empty:
            top_technician = tech_series.index[0]

        # =========================
        # TOP ESTADO
        # =========================

        state_series = (
            df["state"]
            .value_counts()
        )

        if not state_series.empty:
            top_state = state_series.index[0]

    # =====================================
    # DJANGO ORM CHARTS
    # =====================================

    services_by_state = (
        queryset.values("state")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    services_by_type = (
        queryset.values("service_type")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    top_technicians = (
        queryset.values("technician_name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    latest_services = queryset.order_by(
        "-request_datetime"
    )[:10]

    context = {

        # KPIs
        "total_services": total_services,
        "completed_services": completed_services,
        "pending_services": pending_services,
        "total_income": total_income,
        "estimated_profit": estimated_profit,
        "avg_completion_days": avg_completion_days,
        "top_technician": top_technician,
        "top_state": top_state,

        # Charts
        "states_labels": json.dumps([
            item["state"]
            for item in services_by_state
        ]),

        "states_data": json.dumps([
            item["total"]
            for item in services_by_state
        ]),

        "services_labels": json.dumps([
            item["service_type"]
            for item in services_by_type
        ]),

        "services_data": json.dumps([
            item["total"]
            for item in services_by_type
        ]),

        "monthly_labels": json.dumps(
            monthly_labels
        ),

        "monthly_data": json.dumps(
            monthly_data
        ),

        "technicians_labels": json.dumps([
            item["technician_name"]
            for item in top_technicians
        ]),

        "technicians_data": json.dumps([
            item["total"]
            for item in top_technicians
        ]),

        # Table
        "latest_services": latest_services,
    }

    return render(
        request,
        "service_tracking/dashboard.html",
        context,
    )