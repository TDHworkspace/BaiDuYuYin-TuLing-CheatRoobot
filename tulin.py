# -*- coding: utf-8 -*-
import urllib
import json

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

if __name__ == '__main__':

    key = '11f83b13f0784e77a897b1acaec86f33'
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
    while True:
        info = raw_input('我: ')
        request = api + info
        response = getHtml(request)
        dic_json = json.loads(response)
        print '贾维斯：'.decode('utf-8') + dic_json['text']
