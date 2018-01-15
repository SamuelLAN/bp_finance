import urllib2
import funcUtil
import baseObject
import GetData.config.error as error

class Curl(baseObject.base):
    def __init__(self, url, timeout=10):
        self.__uri = url
        self.__request = urllib2.Request(url)
        self.__response = None
        self.__timeout = timeout

    def addHeader(self, key, val):
        self.__request.add_header(key, val)

    def get(self):
        try:
            self.__response = urllib2.urlopen(self.__request, timeout=self.__timeout).read()
        except Exception, ex:
            self.setError(error.CURL)
            print 'Error: uri: ' + self.__uri + ' ' + str(ex)
            funcUtil.write_log('curl', 'uri: ' + self.__uri)
        return self.__response
