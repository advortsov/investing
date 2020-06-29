import requests, bs4
import re
import json 




def GET(url):
    headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    return res

def fin_report(ticker, period_type):
    
    investing_url = "https://www.investing.com"
    res = GET(investing_url+"/search/?q=" + ticker)

    soup = bs4.BeautifulSoup(res.text)
    tickers = soup.select(".js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable script")

    m = re.search('window.allResultsQuotesDataArray = (.+?);', tickers[0].getText())
    found = ''
    if m:
        found = m.group(1)
    j = json.loads(found)
    usa_ticker_href = ''
    pair_id = ''
    for t in j:
        if t['flag'] == 'USA':
            usa_ticker_href = t['link']
            pair_id= str(t['pairId'])
    print(usa_ticker_href)
    print(pair_id)


    res = GET(investing_url+usa_ticker_href+'-income-statement')
    res = GET(investing_url+'/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID='+pair_id+'&report_type=INC&period_type='+period_type)

    print(res)
    return res

report = fin_report('AAPL', 'Annual')
