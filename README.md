# Submarino Price Checker
A python script that scrape submarino's pages and mail the user if prices are as low as the user needs.

## Prerequisites
Submarino Price Checker works fine on python 3.x.
I'm improving it to works on python 2.x too.

## Installing
`$ pip install requests bs4`

## Usage
`$ python scraper.py`

On your first use, you'll need to login on a gmail account and list all products you want to track with their maximum prices.
On your later uses, you'll be allowed to change the email address or password and change the links to track.
If you change the products, all previous products registered will be deleted from urls.txt.

## Creating a custom gmail password
Follow the guide from Google Support
[Google Support](https://support.google.com/accounts/answer/185833?hl=pt-BR)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
