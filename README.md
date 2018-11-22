"# currencies_rest_api" 

## REST API (Exchange rates from RSS feeds)

The application reads RSS feeds with exchange rates from https://www.ecb.europa.eu/home/html/rss.en.html and 
saves them in postgres database. The REST API is written in django.

To run the application, firstly we need to create a postgres database on localhost (port 5432). To do that 
run the following command in command prompt:
```bash
psql -U postgres -h localhost
```
followed by:
```bash
create database currencydb;
```
Now when we have our database running. We can run our application. 
Firstly we need to install all packages from *requirements.txt* on our virtual environment.

Next we should sync to our database for the first time and create an initial user and set a password. 
Firstly go to *exchange_rates/models.py* and comment following code (this code is responsible for 
downloading exchange rates from external service):
```python
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
```
Then:
```bash
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
``` 
Uncomment previously commented code.

Now we can run a server:
```bash
python manage.py runserver 8100
```

Our database will be filled with new exchange rates. If rate for particular currency and date 
exists in db it will not be added.

The database schema:
```python
    currency = models.CharField(max_length=10, null=False)
    date = models.DateField(null=False)
    rate = models.FloatField(null=False)
```
The rate is an equivalent of 1 EUR in given currency.

- To check all exchange rates that are in database go to: <http://localhost:8100/api/exchange-rates/>
- To check exchange rates for particular currency add a currency code to above URL,
eg. for PLN: <http://localhost:8100/api/exchange-rates/PLN/>. Rates are sorted from the latest ones.
- To check rate only for given date: <http://localhost:8100/api/exchange-rates/PLN/2018-11-22/>
- To check rates of all currencies from given date: <http://localhost:8100/api/exchange-rates/2018-11-22/>

You can also manage exchange rates through admin panel (<http://localhost:8100/admin/>). Log in with
credentials provided earlier. 