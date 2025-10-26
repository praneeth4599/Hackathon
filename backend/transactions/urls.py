from django.urls import path
from .views import TransferMoneyView, TransactionHistoryView, FlaggedTransactionsView

app_name = 'transactions'

urlpatterns = [
    path('transfer/', TransferMoneyView.as_view(), name='transfer'),
    path('history/', TransactionHistoryView.as_view(), name='history'),
    path('flagged/', FlaggedTransactionsView.as_view(), name='flagged'),
]
