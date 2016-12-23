import urllib2, json, decimal

# set your preferred currency here
CURRENCY = 'USD' # or 'EUR' or 'GBP'

# create channel here: https://www.pushbullet.com/my-channel
# NOTE: make sure to create a long and random `#tag` for it
CHANNEL = ''

# get your PushBullet Access Token from: https://www.pushbullet.com/#settings/account
TOKEN = ''

def get_price():
    content = urllib2.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json").read()
    data = json.loads(content)

    return decimal.Decimal(data["bpi"][CURRENCY]["rate"])

def notify_pushbullet(msg):
    data = {
        'channel_tag': CHANNEL,
        'type': 'note',
        'title': 'banana',
        'body': msg
    }

    headers = {
        'Content-Type': 'application/json',
        'Access-Token': TOKEN
    }

    req = urllib2.Request('https://api.pushbullet.com/v2/pushes', json.dumps(data), headers)
    resp = urllib2.urlopen(req)
