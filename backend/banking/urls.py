from django.urls import path
from .views import AccountDetailView, CreateAccountView

app_name = 'banking'

urlpatterns = [
    path('account/', AccountDetailView.as_view(), name='account-detail'),
    path('account/create/', CreateAccountView.as_view(), name='account-create'),
]
