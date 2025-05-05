from .utils import dashboard_data
from .decorators import authenticated_only_context


@authenticated_only_context
def global_alerts(request):
    alerts = []
    try:
        alerts = dashboard_data(request).get('alerts', [])
    except Exception:
        alerts = ["Error loading alerts."]
    return {'alerts': alerts}