#!/usr/bin/env python
#encoding=utf-8
import wave
import urllib, urllib2, pycurl
import os,time
import base64
import json
import PyBaiduYuyin as pby
import httplib
import re
import subprocess
import codecs
from lxml import etree
from select import select
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

## ready for baidumusic
reponse = urllib2.urlopen("http://music.baidu.com/songlist")
html = reponse.read()
reponse.close()
tree=etree.HTML(html)
ids =tree.xpath("//a[@sid]/@sid")
names = tree.xpath("//a[@sid]/@title")
url = "http://music.baidu.com/data/music/fmlink?type=mp3&rate=320&songIds="

def control():
        rlist, _, _ = select([sys.stdin], [], [], 1)
        if rlist:
            s = sys.stdin.readline()
            if s[0] == 'n':
                return 'next'
            if s[0] == 'p':
                return 'prev'
	    if s[0] == 'e':
		return 'end'
	
def start(i):
    while i < len(ids):
        playmode = True
	print("贾维斯：正在为您播放：" + names[i] + "，您可以键入n来播放下一曲，键入p来播放上一曲，键入e来结束播放。")
	tts = pby.TTS(app_key="MRFQBZjw0V8D9GArQ5Akh2y7",secret_key="4c499b8b21d0fc600c735265d781228e")
        tts.say('正在为您播放：'.decode('utf-8') + names[i])
	tts = pby.TTS(app_key="MRFQBZjw0V8D9GArQ5Akh2y7",secret_key="4c499b8b21d0fc600c735265d781228e")
        tts.say("您可以键入n来播放下一曲，键入p来播放上一曲，键入e来结束播放。")
        reponses = urllib2.urlopen(url+ids[i])
        htmls = reponses.read()
        song = json.loads(htmls)
        song = song['data']
        song = song['songList']
        song = song[0]
        durations = song['time']
        starttime = time.time()
        player = subprocess.Popen(['mpg123', '-v',song['songLink']], shell=False, universal_newlines=True, stdin=None,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while playmode:
            c = control()
            endtime = time.time()
            usetime = endtime - starttime - durations
            if c == 'next' or usetime > 2:
                player.kill()
                i = i + 1
                break
            if c == 'prev':
                player.kill()
                i = i - 1
                break
	    if c == 'end':
		player.kill()	
		i = len(ids) + 1
		print("贾维斯：正在结束播放，请稍等...")
	  	tts = pby.TTS(app_key="MRFQBZjw0V8D9GArQ5Akh2y7",secret_key="4c499b8b21d0fc600c735265d781228e")
        	tts.say("正在结束播放，请稍等...")
                time.sleep(1)
                break

## get access token by api key & secret key

def get_token():
    apiKey = "MRFQBZjw0V8D9GArQ5Akh2y7"
    secretKey = "4c499b8b21d0fc600c735265d781228e"
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;
    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']
	
##getHtml for tuling

def getHtml(url):
    url = url.encode('utf-8')
    page = urllib.urlopen(url)
    html = page.read()
    return html	
	
def dump_res(buf):
    print buf

luyin = time.time()
def ly():
    os.system('mplayer ty.wav')
    os.system('arecord -D "plughw:1,0" -r 16000 -t wav -d 4 -f S16_LE -c 1  lu/%s.wav'%luyin)	

token = get_token()	

def upurl():
    CE_RATE = 16000
    WAVE_FILE = 'lu/%s.wav'%luyin
    USER_ID = "68-5D-43-F5-62-84"
    WAVE_TYPE = 'wav'
    URL = 'http://vop.baidu.com/server_api'
    #其它参数可参考sdk文档
    f = open(WAVE_FILE,'r')
    speech = base64.b64encode(f.read())
    size = os.path.getsize(WAVE_FILE)
    update = json.dumps({'format':WAVE_TYPE,'rate':CE_RATE,'channel':1,'cuid':USER_ID,'token':token,'speech':speech,'len':size})
    r = urllib2.urlopen(URL,update)
    t = r.read()
    return json.loads(t)

if __name__ == '__main__':

    key = '11f83b13f0784e77a897b1acaec86f33'
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
    while True:
		ly()
		result = upurl()
		print result
		print result[u'err_msg']
		aa = result['result'][0]
		print '我:',
		print aa
		if 'success' in  result[u'err_msg']:
			if u'歌曲，' == aa:
				print ("贾维斯：好的，歌曲马上呈现！")
            			tts = pby.TTS(app_key="MRFQBZjw0V8D9GArQ5Akh2y7",secret_key="4c499b8b21d0fc600c735265d781228e")
            			tts.say("好的，歌曲马上呈现！")
            			time.sleep(1)
				y = 0
				start (y)
				##os.system('mplayer yy/海鸣威-老人与海.mp3')
            			##os.system('mplayer yy/林俊杰-曹操.mp3')
            			##os.system('mplayer yy/张悬-宝贝.mp3')
				time.sleep(1)
			else:		
				info = result['result'][0]
				request = api + info
				response = getHtml(request)
				dic_json = json.loads(response)
				print '贾维斯：'.decode('utf-8') + dic_json['text']
				tts = pby.TTS(app_key="MRFQBZjw0V8D9GArQ5Akh2y7",secret_key="4c499b8b21d0fc600c735265d781228e")
            			tts.say(''.decode('utf-8') + dic_json['text'])	
		##else :	
			##tts = pby.TTS(app_key="MRFQBZjw0V8D9GArQ5Akh2y7",secret_key="4c499b8b21d0fc600c735265d781228e")
	            	##tts.say('贾维斯：很抱歉，没有听清楚，可以重新说一遍吗？')
