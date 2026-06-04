import json
import pandas as pd
from shared.enums.payment_status import PaymentStatus
from shared.enums.service_status import ServiceStatus
from shared.enums.services import Services
from shared.enums.states import States
from datetime import timedelta
from django.utils import timezone
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

    menu_order = 800

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


# =========================
# DASHBOARD
# =========================

def service_dashboard(request):

    queryset = ServiceRequest.objects.all()

    # =====================================
    # FILTERS
    # =====================================

    selected_service = request.GET.get(
        "service_type",
        ""
    )

    selected_status = request.GET.get(
        "service_status",
        ""
    )

    selected_period = request.GET.get(
        "period",
        ""
    )

    selected_state = request.GET.get(
        "state",
        ""
    )

    selected_payment_status = request.GET.get(
        "payment_status",
        ""
    )

    start_date = request.GET.get(
        "start_date",
        ""
    )

    end_date = request.GET.get(
        "end_date",
        ""
    )

    # =====================================
    # SERVICE TYPE
    # =====================================

    if selected_service:

        queryset = queryset.filter(
            service_type=selected_service
        )

    # =====================================
    # STATUS
    # =====================================

    if selected_status:

        queryset = queryset.filter(
            service_status=selected_status
        )

    # =====================================
    # STATE
    # =====================================

    if selected_state:

        queryset = queryset.filter(
            state=selected_state
        )

    # =====================================
    # PAYMENT STATUS
    # =====================================

    if selected_payment_status:

        queryset = queryset.filter(
            payment_status=selected_payment_status
        )
    # =====================================
    # PERIOD
    # =====================================

    # =====================================
    # CUSTOM DATE RANGE
    # =====================================

    if start_date:

        queryset = queryset.filter(
            request_datetime__date__gte=start_date
        )

    if end_date:

        queryset = queryset.filter(
            request_datetime__date__lte=end_date
        )

    now = timezone.now()

    if selected_period == "1m":

        queryset = queryset.filter(
            request_datetime__gte=(
                now - timedelta(days=30)
            )
        )

    elif selected_period == "3m":

        queryset = queryset.filter(
            request_datetime__gte=(
                now - timedelta(days=90)
            )
        )

    elif selected_period == "6m":

        queryset = queryset.filter(
            request_datetime__gte=(
                now - timedelta(days=180)
            )
        )

    elif selected_period == "1y":

        queryset = queryset.filter(
            request_datetime__gte=(
                now - timedelta(days=365)
            )
        )

    # =====================================
    # KPIs
    # =====================================

    total_services = queryset.count()

    completed_services = queryset.filter(
        service_status="completed"
    ).count()

    pending_services = queryset.filter(
        service_status="pending"
    ).count()

    assigned_services = queryset.filter(
        service_status="assigned"
    ).count()

    in_progress_services = queryset.filter(
        service_status="in_progress"
    ).count()

    cancelled_services = queryset.filter(
        service_status="cancelled"
    ).count()

    active_services = queryset.exclude(
        service_status__in=[
            "completed",
            "cancelled",
        ]
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
        "service_status",
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

        # =====================================
        # FECHAS
        # =====================================

        df["request_datetime"] = pd.to_datetime(
            df["request_datetime"]
        )

        df["completion_date"] = pd.to_datetime(
            df["completion_date"]
        )

        # =====================================
        # SERVICIOS POR MES
        # =====================================

        monthly = (
            df.groupby(
                df["request_datetime"].dt.strftime("%Y-%m")
            )
            .size()
            .reset_index(name="total")
        )

        monthly_labels = monthly["request_datetime"].tolist()

        monthly_data = monthly["total"].tolist()

        # =====================================
        # TIEMPO PROMEDIO
        # =====================================

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

        # =====================================
        # TOP TÉCNICO
        # =====================================

        tech_series = (
            df["technician_name"]
            .value_counts()
        )

        if not tech_series.empty:
            top_technician = tech_series.index[0]

        # =====================================
        # TOP ESTADO
        # =====================================

        state_series = (
            df["state"]
            .value_counts()
        )

        if not state_series.empty:

            top_state_key = state_series.index[0]

            top_state = dict(States.choices).get(
                top_state_key,
                top_state_key
            )

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

    services_by_status = (
        queryset.values("service_status")
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

    # =====================================
    # CONTEXT
    # =====================================

    context = {

        # KPIs
        "total_services": total_services,
        "pending_services": pending_services,
        "assigned_services": assigned_services,
        "in_progress_services": in_progress_services,
        "completed_services": completed_services,
        "cancelled_services": cancelled_services,
        "active_services": active_services,

        "total_income": total_income,
        "estimated_profit": estimated_profit,

        "avg_completion_days": avg_completion_days,

        "top_technician": top_technician,
        "top_state": top_state,

        # =====================================
        # FILTER OPTIONS
        # =====================================

        "service_options": Services.choices,

        "status_options": ServiceStatus.choices,

        "state_options": States.choices,

        "selected_service": selected_service,

        "selected_status": selected_status,

        "selected_state": selected_state,

        "selected_payment_status": selected_payment_status,

        "selected_period": selected_period,

        "start_date": start_date,

        "end_date": end_date,

        "payment_status_options": PaymentStatus.choices,
        # =====================================
        # CHARTS
        # =====================================

        "states_labels": json.dumps([
            dict(States.choices).get(
                item["state"],
                item["state"]
            )
            for item in services_by_state
        ]),

        "states_data": json.dumps([
            item["total"]
            for item in services_by_state
        ]),

        "services_labels": json.dumps([
            dict(Services.choices).get(
                item["service_type"],
                item["service_type"]
            )
            for item in services_by_type
        ]),



        "services_data": json.dumps([
            item["total"]
            for item in services_by_type
        ]),

        "status_labels": json.dumps([
            dict(ServiceStatus.choices).get(
                item["service_status"],
                item["service_status"]
            )
            for item in services_by_status
        ]),

        "status_data": json.dumps([
            item["total"]
            for item in services_by_status
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

        # =====================================
        # TABLE
        # =====================================

        "latest_services": latest_services,
    }

    return render(
        request,
        "service_tracking/dashboard.html",
        context,
    )