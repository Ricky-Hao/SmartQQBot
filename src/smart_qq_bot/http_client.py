import requests
import time
import os
import http.cookiejar
from smart_qq_bot.logger import logger

from smart_qq_bot.config import (
    SMART_QQ_REFER,
    COOKIE_FILE,
)
from smart_qq_bot.exceptions import ServerResponseEmpty


class HttpClient(object):
    def __init__(self, load_cookie=False, cookie_file=COOKIE_FILE):
        if not os.path.isdir("./cookie"):
            os.mkdir("./cookie")
        self._cookie = self.get_cookiejar(cookie_file)
        self._opener = self.get_opener()
        if load_cookie:
            self.load_cookie()

    def get_cookiejar(self, cookie_file):
        return http.cookiejar.LWPCookieJar(cookie_file)

    def get_opener(self):
        _s=requests.Session()
        _s.cookies=self._cookie
        _s.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            'Referer': 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
        }
        return _s

    def load_cookie(self):
        try:
            self._cookie.load(ignore_discard=True, ignore_expires=True)
        except Exception:
            self._cookie.save(ignore_discard=True, ignore_expires=True)

    @staticmethod
    def get_timestamp():
        return str(int(time.time()*1000))

    def get(self, url, refer=None):
        try:
            req = requests.get(url,headers={"Referer":refer or SMART_QQ_REFER})
            tmp_req = self._opener.get(url,headers={"Referer":refer or SMART_QQ_REFER})
            self._cookie.save(COOKIE_FILE, ignore_discard=True,ignore_expires=True)
            #logger.debug(tmp_req.text)
            return tmp_req.text
        except requests.HTTPError as e:
            logger.debug(e)
            return e

    def post(self, url, data, refer=None):
        try:
            req = requests.post(url, data=data,headers={'Referer':refer or SMART_QQ_REFER})
            try:
                tmp_req = self._opener.post(url, data=data,headers={'Referer':refer or SMART_QQ_REFER}, timeout=180)
            except requests.HTTPError:
                raise ServerResponseEmpty("Server response error, check the network connections: %s" % url)
            self._cookie.save(COOKIE_FILE, ignore_discard=True, ignore_expires=True)
            return tmp_req.text
        except requests.HTTPError as e:
            return e
    
    def get_cookie(self, key):
        for c in self._cookie:
            if c.name == key:
                return c.value
        return ''

    def set_cookie(self, key, val, domain):
        ck = http.cookiejar.Cookie(
            version=0, name=key, value=val, port=None, port_specified=False, domain=domain,
            domain_specified=False, domain_initial_dot=False, path='/', path_specified=True,
            secure=False, expires=None, discard=True, comment=None, comment_url=None,
            rest={'HttpOnly': None}, rfc2109=False
        )
        self._cookie.set_cookie(ck)
        self._cookie.save(ignore_discard=True, ignore_expires=True)

    # @staticmethod
    def download(self, url, file):
        output = open(file, 'wb')
        output.write(self._opener.get(url).content)
        output.close()
