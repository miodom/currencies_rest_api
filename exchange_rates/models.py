from django.db import models

import feedparser

CURRENCIES = ["usd", "jpy", "bgn", "czk", "dkk", "eek", "gbp", "huf", "pln", "ron", "sek", "chf",
              "isk", "nok", "hrk", "rub", "try", "aud", "brl", "cad", "cny", "hkd", "idr", "inr",
              "krw", "mxn", "myr", "nzd", "php", "sgd", "thb", "zar"]


class ExchangeRates(models.Model):
    currency = models.CharField(max_length=10, null=False)
    date = models.DateField(null=False)
    rate = models.FloatField(null=False)

    def __str__(self):
        return "{date}: 1 EUR = {rate} {currency}".format(date=self.date, rate=self.rate, currency=self.currency)

    @classmethod
    def download_exchange_rates(cls):
        for currency in CURRENCIES:
            currency_feed = feedparser.parse("https://www.ecb.europa.eu/rss/fxref-{}.html".format(currency))
            for entry in currency_feed.entries:
                currency_name = entry["cb_targetcurrency"]
                date = entry["updated"][:10]
                rate = entry["cb_exchangerate"].split('\n', 1)[0]
                try:
                    cur = cls.objects.get(currency=currency_name, date=date)
                except cls.DoesNotExist:
                    cur = cls(currency=currency_name, date=date, rate=rate)
                    cur.save()


ExchangeRates.download_exchange_rates()

