"""
Middleware for automatic audit logging of HTTP requests.
Logs important actions automatically without explicit calls.
"""

from .models import AuditLog


def get_client_ip(request):
    """Extract client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AuditMiddleware:
    """
    Middleware to log important requests automatically.
    Can be extended to log all requests for compliance.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log after response is generated
        if request.user.is_authenticated:
            # Determine action based on path
            action = None
            if '/api/auth/login/' in request.path and request.method == 'POST':
                action = 'login' if response.status_code == 200 else 'failed_login'
            elif '/api/transactions/transfer/' in request.path and request.method == 'POST':
                if response.status_code == 200:
                    action = 'transfer'

            if action:
                AuditLog.objects.create(
                    user=request.user,
                    action=action,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    status='success' if response.status_code < 400 else 'failed'
                )

        return response
