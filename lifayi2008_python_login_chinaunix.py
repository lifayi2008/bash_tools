#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
import re
import urllib
import urllib2
import cookielib

def get_value(name, string):
        if name == 'loginhash':
                pattern_line = re.search(r'.*loginhash=(?P<value>.*?)".*', string)
        else:
                pattern_line = re.search(r'.*name="'+name+'".*?value="(?P<value>.*?)".*', string)
        if(pattern_line):
                value = pattern_line.group("value")
                return value


def get_hashvalue():
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        chinaunix = opener.open(login_url)
        html = chinaunix.read()
        chinaunix.close()

        login_info={}
        login_info['formhash'] = get_value('formhash', html)
        login_info['referer'] = get_value('referer', html)
        login_info['loginsubmit'] = get_value('loginsubmit', html)
        login_info['return_type'] = get_value('return_type', html)

        loginhash = get_value('loginhash', html)

        return loginhash,login_info,opener

def login(username, password, login_info, **logindata):
        login_info['username'] = username
        login_info['password'] = password

        post_data = urllib.urlencode(login_info)
        post_url = 'http://bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash='+loginhash
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}

        request = urllib2.Request(url = post_url, data = post_data, headers = header)
        response = opener.open(request)
        response.close()

def get_homeurl():
        response2 = opener.open('http://bbs.chinaunix.net')
        bbs_html = response2.read()
        response2.close()

        match_line = re.search(r'.*你好.*?href="(?P<home_id>.*?)".*', bbs_html.decode('gbk').encode('utf-8'))
        if match_line==None:
                print 'response2 error'
                sys.exit(1)

        home_url = 'http://bbs.chinaunix.net/'+match_line.group("home_id")
        return home_url


def get_score(home_url):
        response3 = opener.open(home_url)
        home_html = response3.read()
        response3.close()

        match_line2 = re.search(r'.*可用积分.*?(?P<score>[0-9]+).*', home_html.decode('gbk').encode('utf-8'))
        if match_line2==None:
                print 'response3 error'
                sys.exit(1)

        return match_line2.group("score")

if __name__ == '__main__':
        login_url = 'http://bbs.chinaunix.net/member.php?mod=logging&action=login&logsubmit=yes&return_type=1'
        loginhash,login_info,opener = get_hashvalue()
        login(username="你的用户名", password="你的密码", login_info=login_info, loginhash=loginhash)
        home_url = get_homeurl()
        print '你当前的可用积分为：'+get_score(home_url)