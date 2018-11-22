from rest_framework import generics
from .models import ExchangeRates
from .serializers import ExchangeRatesSerializer


class ListExchangeRatesView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = ExchangeRates.objects.all().order_by('-date', 'currency')
    serializer_class = ExchangeRatesSerializer


class ListAllCurrencyRatesView(generics.ListAPIView):
    def get_queryset(self):
        if len(self.kwargs['param']) == 3:
            return ExchangeRates.objects.filter(currency=self.kwargs['param']).order_by('-date')
        else:
            return ExchangeRates.objects.filter(date=self.kwargs['param']).order_by('currency')
    serializer_class = ExchangeRatesSerializer


class ListCurrencyRateFromGivenDateView(generics.ListAPIView):
    def get_queryset(self):
        return ExchangeRates.objects.filter(currency=self.kwargs['currency'], date=self.kwargs['date'])
    serializer_class = ExchangeRatesSerializer
