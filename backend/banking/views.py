from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import BankAccount
from .serializers import BankAccountSerializer


class AccountDetailView(generics.RetrieveAPIView):
    """Get user's bank account details"""
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.bank_account


class CreateAccountView(generics.CreateAPIView):
    """Create a new bank account for user"""
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Check if user already has an account
        if hasattr(request.user, 'bank_account'):
            return Response(
                {'error': 'User already has a bank account'},
                status=status.HTTP_400_BAD_REQUEST
            )

        account = BankAccount.objects.create(
            user=request.user,
            account_type=request.data.get('account_type', 'savings')
        )

        serializer = self.get_serializer(account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
