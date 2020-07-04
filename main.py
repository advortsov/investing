import requests
import bs4
import re
import json


investing_url = "https://www.investing.com"

def GET(url):
    print('GET: ' + url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res

def get_pair_id(ticker):
    res = GET(investing_url+"/search/?q=" + ticker)
    soup = bs4.BeautifulSoup(res.text, features="html5lib")
    tickers = soup.select(".js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable script")
    print('tickers: ' + str(tickers))
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
    res = GET(investing_url+'/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=' +
              pair_id+'&report_type='+report_type+'&period_type='+period_type)
    return res


def parse_bal(report):
    pass

def parse_inc(report):
    if report == None:
        print('Report is empty')
    else:
        soup = bs4.BeautifulSoup(report.text, features="html5lib")
        t = soup.find('table')
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


for t in ['AAPL', 'MCD', 'ACN', 'V', 'TXN']:
    print(t)
    isd = parse_inc(report(get_pair_id(t), 'INC', 'Annual'))
    print(relative(isd['Revenue']))
