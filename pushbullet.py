#!/usr/bin/python
# -*- coding: UTF-8 -*-

# set your preferred currency here
CURRENCY = 'USD' # or 'EUR' or 'GBP'

# Set this to `False` to see value in Bitcoin instead
SATOSHI = True

# create channel here: https://www.pushbullet.com/my-channel
# NOTE: make sure to create a long and random `#tag` for it
CHANNEL = ''

# get your PushBullet Access Token from: https://www.pushbullet.com/#settings/account
TOKEN = ''

#
## NO NEED TO TOUCH STUFF BELOW ;)
#
import urllib2, json, decimal

def get_price():
    content = urllib2.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json").read()
    data = json.loads(content)

    return decimal.Decimal(data["bpi"][CURRENCY]["rate"])

def get_currency_sign():
    if CURRENCY == 'USD':
        return '$'
    elif CURRENCY == 'EUR':
        return '€'
    elif CURRENCY == 'GBP':
        return '£'

def notify_pushbullet(fee, txfee):
    earned = decimal.Decimal(fee - txfee)
    earned_btc = earned / decimal.Decimal(100000000)

    earned_str = str(earned if SATOSHI else earned_btc)
    if SATOSHI:
        earned_str += ' Satoshi'
    else:
        earned_str += 'BTC'

    data = {
        'channel_tag': CHANNEL,
        'type': 'note',
        'title': '{0} earned!'.format(earned_str),
        'body': 'Which is around {0}{1:.4f} as of now'.format(get_currency_sign(), float(earned_btc * get_price()))
    }

    headers = {
        'Content-Type': 'application/json',
        'Access-Token': TOKEN
    }

    req = urllib2.Request('https://api.pushbullet.com/v2/pushes', json.dumps(data), headers)
    resp = urllib2.urlopen(req)
