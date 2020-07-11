import requests
import bs4
import re
import json
import time
import jsonpickle

pp = '/mnt/c/Users/alxdv/Desktop/pys/investing/'
db = {}
ticker_to_pair_id = {}
investing_url = "https://www.investing.com"
tickers_for_retry = []

def GET(url):
    print('GET: ' + url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    res = requests.get(url, headers=headers, timeout=5)
    res.raise_for_status()
    return res


def get_pair_id(ticker):
    try:
        res = GET(investing_url+"/search/?q=" + ticker)
    except requests.exceptions.ConnectTimeout:
        print("Connect Timeout occurred")
        time.sleep(15)
        tickers_for_retry.append(ticker)
        return None
    except requests.exceptions.Timeout:
        print("Timeout occurred")
        time.sleep(15)
        tickers_for_retry.append(ticker)
        return None
    soup = bs4.BeautifulSoup(res.text, features="html5lib")
    tickers = soup.select(
        ".js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable script")
    #print('tickers: ' + str(tickers))
    if len(tickers) == 0:
        return None
    m = re.search('window.allResultsQuotesDataArray = (.+?);',
                  tickers[0].getText())
    found = ''
    if m:
        found = m.group(1)
    j = json.loads(found)
    usa_ticker_href = ''
    pair_id = ''
    for t in j:
        if t['flag'] == 'USA':
            usa_ticker_href = t['link']
            pair_id = str(t['pairId'])
            break
    print(usa_ticker_href)
    print(pair_id)
    return pair_id


def report(pair_id, report_type, period_type):
   #res = GET(investing_url+usa_ticker_href+'-income-statement')
    # https://www.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=7884&report_type=BAL&period_type=Annual
    try:
      res = GET(investing_url+'/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=' +
              pair_id+'&report_type='+report_type+'&period_type='+period_type)
    except requests.exceptions.ConnectTimeout:
        print("Connect Timeout occurred")
        time.sleep(15)
        #tickers_for_retry.append(ticker)
        return None
    return res


def parse_bal(report):
    pass


def parse_inc(report):
    if report == None:
        print('Report is empty')
    else:
        soup = bs4.BeautifulSoup(report.text, features="html5lib")
        t = soup.find('table')
        if t is None:
            return None
        rows_tags = t.find_all(lambda tag: tag.name == 'td' and not tag.attrs)
        d = {}
        name = ''
        for rt in rows_tags:
            if len(rt) == 0:
                continue
            inner_spans = rt.select('span')
            if len(inner_spans) != 0:
                name = inner_spans[0].text
                d[name] = []
            else:
                d[name].append(rt.text)
        return d


def relative(row):
    return [float(row[i]) / float(row[i+1]) for i in range(len(row)-1)]


"""
Financials
Financial Summary
Income Statement
Balance Sheet
Cash Flow
Ratios
Dividends
Earnings
"""

class Financials():
  def __init__(self, pair_id, income_statement):
    self.pair_id = pair_id
    self.income_statement = income_statement
#    self.income_statement = json.dumps(income_statement.__dict__, indent=2)
  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__)

f = Financials('6376', parse_inc(report('6376', 'INC', 'Annual')))
print(jsonpickle.encode(f))

ticker_to_pair_id= {}
with open(pp+'tickers_with_pair_ids.txt') as f:
    s = f.read()
    ticker_to_pair_id = json.loads(s)



for k,v in ticker_to_pair_id.items():
    if v is not None and v != '':
        print(k)
        db[k] = Financials(v, parse_inc(report(v, 'INC', 'Annual')))

print(db)
with open(pp+'db.json', 'w') as f:
    f.write(jsonpickle.encode(db))

db={}
with open('tickers.txt') as f:
  data = f.readlines()
  db = jsonpickle.decode(data)

"""
time.sleep(1)
with open('tickers.txt') as f:
    tickers = f.readlines()
    for t in tickers:
        t = t.rstrip('\r\n')
        if t not in dump or dump[t] == None or dump[t] == '':
            print(t)
            ticker_to_pair_id[t]= get_pair_id(t)
        else:
            print(t + ' already in dump')

print(ticker_to_pair_id)

print('Retrying with ' + str(tickers_for_retry))
time.sleep(300)
print('Now!')
for t in tickers_for_retry:
    print(t.rstrip('\r\n'))
    ticker_to_pair_id[t.rstrip('\r\n')] = get_pair_id(t)


with open('tickers_with_pair_ids.txt', 'w') as f:
    f.write(json.dumps(ticker_to_pair_id, indent=4))

time.sleep(1)
with open('tickers.txt') as f:
    tickers = f.readlines()
    for t in tickers:
        t = t.rstrip('\r\n')
        if t not in dump or dump[t] == None or dump[t] == '':
            print(t)
            ticker_to_pair_id[t]= get_pair_id(t)
        else:
            print(t + ' already in dump')

print(ticker_to_pair_id)

print('Retrying with ' + str(tickers_for_retry))
time.sleep(300)
print('Now!')
for t in tickers_for_retry:
    print(t.rstrip('\r\n'))
    ticker_to_pair_id[t.rstrip('\r\n')] = get_pair_id(t)


with open('tickers_with_pair_ids.txt', 'w') as f:
    f.write(json.dumps(ticker_to_pair_id, indent=4))
"""

"""
{
  "pair_id": "6376",
  "income_statement": {
    "Total Revenue": [
      "19573",
      "22611",
      "22258",
      "23554"
    ],
    "Revenue": [
      "19573",
      "22611",
      "22258",
      "23554"
    ],
    "Other Revenue, Total": [
      "-",
      "-",
      "-",
      "-"
    ],
    "Cost of Revenue, Total": [
      "8599",
      "10244",
      "9792",
      "9315"
    ],
    "Gross Profit": [
      "10974",
      "12367",
      "12466",
      "14239"
    ],
    "Total Operating Expenses": [
      "12041",
      "22065",
      "19854",
      "17239"
    ],
    "Selling/General/Admin. Expenses, Total": [
      "2195",
      "2986",
      "2658",
      "2213"
    ],
    "Research & Development": [
      "5398",
      "5625",
      "5485",
      "5141"
    ],
    "Depreciation / Amortization": [
      "-",
      "-",
      "-",
      "-"
    ],
    "Interest Expense (Income) - Net Operating": [
      "-",
      "-",
      "-",
      "-"
    ],
    "Unusual Expense (Income)": [
      "-4151",
      "3228",
      "1919",
      "214"
    ],
    "Other Operating Expenses, Total": [
      "-",
      "-18",
      "37",
      "356"
    ],
    "Operating Income": [
      "7532",
      "546",
      "2404",
      "6315"
    ],
    "Interest Income (Expense), Net Non-Operating": [
      "-51",
      "-154",
      "583",
      "518"
    ],
    "Gain (Loss) on Sale of Assets": [
      "-",
      "-",
      "-",
      "-"
    ],
    "Other, Net": [
      "-",
      "-",
      "-",
      "-"
    ],
    "Net Income Before Taxes": [
      "7481",
      "392",
      "2987",
      "6833"
    ],
    "Provision for Income Taxes": [
      "3095",
      "4913",
      "543",
      "1131"
    ],
    "Net Income After Taxes": [
      "4386",
      "-4521",
      "2444",
      "5702"
    ],
    "Minority Interest": [
      "-",
      "-",
      "1",
      "3"
    ],
    "Equity In Affiliates": [
      "-",
      "-",
      "-",
      "-"
    ],
    "U.S GAAP Adjustment": [
      "-",
      "-",
      "-",
      "-"
    ],
    "Net Income Before Extraordinary Items": [
      "4386",
      "-4521",
      "2445",
      "5705"
    ],
    "Total Extraordinary Items": [
      "-",
      "-443",
      "-",
      "-"
    ],
    "Net Income": [
      "4386",
      "-4964",
      "2445",
      "5705"
    ],
    "Total Adjustments to Net Income": [
      "-",
      "-",
      "-",
      "-"
    ],
    "Income Available to Common Excluding Extraordinary Items": [
      "4386",
      "-4521",
      "2445",
      "5705"
    ],
    "Dilution Adjustment": [
      "-",
      "-",
      "-",
      "-"
    ],
    "Diluted Net Income": [
      "4386",
      "-4964",
      "2445",
      "5705"
    ],
    "Diluted Weighted Average Shares": [
      "1220",
      "1463",
      "1490",
      "1498"
    ],
    "Diluted EPS Excluding Extraordinary Items": [
      "3.6",
      "-3.09",
      "1.64",
      "3.81"
    ],
    "DPS - Common Stock Primary Issue": [
      "2.48",
      "2.43",
      "2.2",
      "2.02"
    ],
    "Diluted Normalized EPS": [
      "1.6",
      "-1.66",
      "2.69",
      "3.93"
    ]
  }
}
"""
