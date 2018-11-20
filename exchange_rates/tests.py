from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import ExchangeRates
from .serializers import ExchangeRatesSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def add_exchange_rate(currency="", date="", rate=""):
        if currency != "" and date != "" and rate != "":
            ExchangeRates.objects.create(currency=currency, date=date, rate=rate)

    def setUp(self):
        # add test data
        self.add_exchange_rate("PLN", "2018-11-09", "4.3456")
        self.add_exchange_rate("USD", "2018-11-09", "0.9999")
        self.add_exchange_rate("PLN", "2018-11-07", "4.2690")
        self.add_exchange_rate("PLN", "2018-11-06", "4.3800")


class GetAllExchangeRatesTest(BaseViewTest):

    def test_get_all_exchange_rates(self):
        """
        This test ensures that all exchange rates added in the setUp method
        exist when we make a GET request to the exchange_rates/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("exchange-rates-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = ExchangeRates.objects.all()
        serialized = ExchangeRatesSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
