#encoding:utf-8
import pymongo
import re
import requests
from lxml import etree


def get_response(url):
    i = 0
    while True:
        if i>5:
            return
        try:
            response = requests.get(url, headers=headers,timeout=30).text
            return response
        except:
            i+=1
            continue

MONGODB_URI = 'mongodb://127.0.0.1:27017'
url = "http://www.listyourleave.com/wp-admin/admin-ajax.php"
headers={
"Accept":"*/*",
"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Content-Length":"43",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"Cookie":"PHPSESSID=9hnrce5acvpfnaiovk3pr9s811; __utma=53010869.1180931113.1594730655.1594730655.1594730655.1; __utmc=53010869; __utmz=53010869.1594730655.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=53010869.6.10.1594730655",
"Host":"www.listyourleave.com",
"Pragma":"no-cache",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
"X-Requested-With":"XMLHttpRequest",
}

al_list = ["A",'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
for al in al_list:
    data = {
    "action":"companies_list_ajax_request",
    "sortBy":al,
    }
    response = requests.post(url,headers=headers,data=data).text
    mongo_client = pymongo.MongoClient(MONGODB_URI).listyourleave.company
    company_urls = re.findall(r'href="(http://www\.listyourleave\.com/company/\?website=.*?)">(.*?)<',response)
    print(company_urls)
    for company_url in company_urls:
        response2 = get_response(company_url[0])
        html = etree.HTML(response2)
        company = company_url[-1]
        Weekspaid1 = html.xpath('//td[@data-th="# Weeks off fully paid (100% salary)"]/text()')
        Weekspaid2 = html.xpath('//td[@data-th="# Weeks off partially paid (some portion of salary)"]/text()')
        Weekspaid3 = html.xpath('//td[@data-th="% of partial salary paid"]/text()')
        Weekspaid4 = html.xpath('//td[@data-th="# Weeks with no pay"]/text()')
        Weekspaid5 = html.xpath('//td[@data-th="Total Weeks off with leave policy"]/text()')
        item = {}
        item['company'] = company
        item['wks_fully_paid'] = int(Weekspaid1[0]) if Weekspaid1 else "N/A"
        item['wks_part_paid'] = int(Weekspaid2[0]) if Weekspaid2 else "N/A"
        item['pct_part_salary'] = int(Weekspaid3[0]) if Weekspaid3 else "N/A"
        item['wks_no_pay'] = int(Weekspaid4[0]) if Weekspaid4 else "N/A"
        item['tot_wks_leave'] = int(Weekspaid5[0]) if Weekspaid5 else "N/A"
        item['emp_leave_rating'] = "N/A"
        result = mongo_client.find_one({"company":company})
        if not result:
            mongo_client.insert_one(item)
