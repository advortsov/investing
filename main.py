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

def income_statement(ticker, period_type):
    investing_url = "https://www.investing.com"
    res = GET(investing_url+"/search/?q=" + ticker)
    soup = bs4.BeautifulSoup(res.text,features="html5lib")
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
    return res

def parse(report):
    soup = bs4.BeautifulSoup(report.text, features="html5lib")

    t = soup.find('table')
    rows_tags = t.find_all(lambda tag: tag.name == 'td' and not tag.attrs)
    d = {}
    name = '' 
    for rt in rows_tags:
        if len(rt) == 0:
            continue
        inner_spans = rt.select('span')
        if len(inner_spans)!= 0:
            name = inner_spans[0].text
            d[name] = []
        else:
            d[name].append(rt.text)
    return d

report = income_statement('AAPL', 'Annual')
income_statement_dict = parse(report)
"""
<table class="genTbl reportTbl">
    <tr class="alignBottom" id="header_row">
			  <th><span class="lightgrayFont arial_11 noBold">Period Ending:</span></th>
                 <th><span class="bold">2019</span><div class="noBold arial_11">28/09</div></th>
                 <th><span class="bold">2018</span><div class="noBold arial_11">29/09</div></th>
                 <th><span class="bold">2017</span><div class="noBold arial_11">30/09</div></th>
                 <th><span class="bold">2016</span><div class="noBold arial_11">24/09</div></th>

             </tr>
        </thead>
    <tbody>
        <tr class="openTr pointer" id="parentTr">
        <td><span class=" bold">Total Revenue<span class="dropDownArrowLightGray"></span></span></td>
        <td>260174</td>
        <td>265595</td>
        <td>229234</td>
        <td>215639</td>
    </tr><tr class="noHover" id="childTr"><td colspan="5" class="innerTD"><div><table class="genTbl reportTbl"><tbody>            <tr class="child">
        <td><span class="">Revenue</span></td>
        <td>260174</td>
        <td>265595</td>
        <td>229234</td>
        <td>215639</td>
    </tr>            <tr class="child last">
        <td><span class="">Other Revenue, Total</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr></tbody></table></div></td></tr>            <tr>
        <td><span class="">Cost of Revenue, Total</span></td>
        <td>161782</td>
        <td>163756</td>
        <td>141048</td>
        <td>131376</td>
    </tr>            <tr>
        <td><span class=" bold">Gross Profit</span></td>
        <td>98392</td>
        <td>101839</td>
        <td>88186</td>
        <td>84263</td>
    </tr>            <tr class="openTr pointer" id="parentTr">
        <td><span class=" bold">Total Operating Expenses<span class="dropDownArrowLightGray"></span></span></td>
        <td>196244</td>
        <td>194697</td>
        <td>167890</td>
        <td>155615</td>
    </tr><tr class="noHover" id="childTr"><td colspan="5" class="innerTD"><div><table class="genTbl reportTbl"><tbody>            <tr class="child">
        <td><span class="">Selling/General/Admin. Expenses, Total</span></td>
        <td>18245</td>
        <td>16705</td>
        <td>15261</td>
        <td>14194</td>
    </tr>            <tr class="child">
        <td><span class="">Research & Development</span></td>
        <td>16217</td>
        <td>14236</td>
        <td>11581</td>
        <td>10045</td>
    </tr>            <tr class="child">
        <td><span class="">Depreciation / Amortization</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>            <tr class="child">
        <td><span class="">Interest Expense (Income) - Net Operating</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>            <tr class="child">
        <td><span class="">Unusual Expense (Income)</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>            <tr class="child last">
        <td><span class="">Other Operating Expenses, Total</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr></tbody></table></div></td></tr>            <tr>
        <td><span class=" bold">Operating Income</span></td>
        <td>63930</td>
        <td>70898</td>
        <td>61344</td>
        <td>60024</td>
    </tr>            <tr>
        <td><span class="">Interest Income (Expense), Net Non-Operating</span></td>
        <td>1385</td>
        <td>2446</td>
        <td>2878</td>
        <td>2543</td>
    </tr>            <tr>
        <td><span class="">Gain (Loss) on Sale of Assets</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>            <tr>
        <td><span class="">Other, Net</span></td>
        <td>422</td>
        <td>-441</td>
        <td>-133</td>
        <td>-1195</td>
    </tr>            <tr>
        <td><span class=" bold">Net Income Before Taxes</span></td>
        <td>65737</td>
        <td>72903</td>
        <td>64089</td>
        <td>61372</td>
    </tr>            <tr>
        <td><span class="">Provision for Income Taxes</span></td>
        <td>10481</td>
        <td>11857</td>
        <td>15738</td>
        <td>15685</td>
    </tr>            <tr>
        <td><span class=" bold">Net Income After Taxes</span></td>
        <td>55256</td>
        <td>61046</td>
        <td>48351</td>
        <td>45687</td>
    </tr>            <tr>
        <td><span class="">Minority Interest</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>            <tr>
        <td><span class="">Equity In Affiliates</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>            <tr>
        <td><span class="">U.S GAAP Adjustment</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>            <tr>
        <td><span class=" bold">Net Income Before Extraordinary Items</span></td>
        <td>55256</td>
        <td>61046</td>
        <td>48351</td>
        <td>45687</td>
    </tr>            <tr>
        <td><span class="">Total Extraordinary Items</span></td>
        <td>-</td>
        <td>-1515</td>
        <td>-</td>
        <td>-</td>
    </tr>            <tr>
        <td><span class=" bold">Net Income</span></td>
        <td>55256</td>
        <td>59531</td>
        <td>48351</td>
        <td>45687</td>
    </tr>            <tr>
        <td><span class="">Total Adjustments to Net Income</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>            <tr>
        <td><span class=" bold">Income Available to Common Excluding Extraordinary Items</span></td>
        <td>55256</td>
        <td>61046</td>
        <td>48351</td>
        <td>45687</td>
    </tr>            <tr>
        <td><span class="">Dilution Adjustment</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>            <tr>
        <td><span class="">Diluted Net Income</span></td>
        <td>55256</td>
        <td>59531</td>
        <td>48351</td>
        <td>45687</td>
    </tr>            <tr>
        <td><span class="">Diluted Weighted Average Shares</span></td>
        <td>4648.91</td>
        <td>5000.11</td>
        <td>5251.69</td>
        <td>5500.28</td>
    </tr>            <tr>
        <td><span class=" bold">Diluted EPS Excluding Extraordinary Items</span></td>
        <td>11.89</td>
        <td>12.21</td>
        <td>9.21</td>
        <td>8.31</td>
    </tr>            <tr>
        <td><span class="">DPS - Common Stock Primary Issue</span></td>
        <td>3</td>
        <td>2.72</td>
        <td>2.4</td>
        <td>2.18</td>
    </tr>            <tr>
        <td><span class="">Diluted Normalized EPS</span></td>
        <td>11.89</td>
        <td>12.21</td>
        <td>9.21</td>
        <td>8.31</td>
    </tr>            </tbody>

</table>


"""
