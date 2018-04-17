#coding=utf-8
from bs4 import BeautifulSoup
import requests

btm_headers = {
    'Referer': 'https://otcbtc.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
seller_headers = {
    'Referer': 'https://otcbtc.com/sell_offers?currency=btm&fiat_currency=cny&payment_type=all',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

baseurl = 'https://otcbtc.com/'


def getcheapestobc():
	url = 'https://otcbtc.com/sell_offers?currency=btm&fiat_currency=cny&payment_type=all'
	btm_data = requests.get(url,headers=btm_headers)
	btm_soup = BeautifulSoup(btm_data.text,'lxml')
	cheapest = btm_soup.select('.recommend-card__price')[0].get_text()
	cheapesturl = btm_soup.select('a.btn.btn-theme')[0].get('href')
	print('cheapest price: '+cheapest+'  buyurl: '+cheapesturl)

	buycheapestobc(cheapesturl)

def buycheapestobc(cheapesturl):
	seller_data = requests.get(baseurl+cheapesturl,headers=seller_headers)
	seller_soup = BeautifulSoup(seller_data.text,'lxml')
	seller_range = seller_soup.select('input#order_fiat_currency_amount')[0].get('data-parsley-range')
	print('seller_range: '+seller_range)
	seller_payment_type = seller_soup.select('select.select.optional.form-control option')
	print(seller_payment_type)

def obclogin():
	login_headers = {
		'Origin': 'https://otcbtc.com',
    	'Referer': 'https://otcbtc.com/sign_in',
    	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

	loginurl = 'https://otcbtc.com/sign_in'

	loginhtml = requests.get(loginurl,headers=login_headers)
	authtoken = BeautifulSoup(loginhtml.text,'lxml').select('input[type="hidden"]')[1].get('value')
	formData = {
				'user[email]':'4324@qq.com',
				'user[password]':'abcd',
				'authenticity_token':authtoken,
				'utf8':'%E2%9C%93',
				'commit':'%E7%99%BB+%E5%BD%95'
				}
	session = requests.session()
	loginresult = session.post(loginurl, data=formData)
obclogin()
#getcheapestobc()



