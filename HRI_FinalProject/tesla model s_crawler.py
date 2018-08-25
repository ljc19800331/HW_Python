# -*- coding:utf-8 -*-
import urllib
import urllib2
import zlib
import re
import time
import json
from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1

# content filter
class Tool:
    remove = re.compile('<p>|</p>|<a.*?>|</a>|', re.S)       #regular expression
    replacebr = re.compile('<br />', re.S)                   #define replacebr with regular expression
    def replace(self,x):                                     #define methods
        x = re.sub(self.remove, "", x)                       #define re.sub=substitude
        x = re.sub(self.replacebr, " ", x)
        # strip()将前后多余内容删除
        return x.strip()

# Thread list
class LIST:
    # initialization input baseurl
    def __init__(self, baseUrl):
        self.baseURL = baseUrl

    # get list page
    def getPage(self, pageNum):
        try:
            url = self.baseURL + '?page=' + str(pageNum-1)
            '''request = urllib2.Request(url)
            request.add_header('Accept-encoding', 'gzip')
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
            request.add_header('Host','teslamotorsclub.com')
            request.add_header('Referer',
                               'https://teslamotorsclub.com/tmc/forums/model-s-ordering-production-delivery.112/')
            request.add_header('GET', url)'''
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            response = opener.open(url)
            content = response.read()
            gzipped = response.headers.get('Content-Encoding')
            if gzipped:
                content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
            return content
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"Connection Failed", e.reason
                return None

    # get total pageNum
    def getPageNum(self, page):
        pattern = re.compile('pager-last.*?><.*?page=(.*?)">', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return 1

    # get thread title
    def getTitle(self, page):
        pattern = re.compile('forum/forums/(.*?)">', re.S)
        items = re.findall(pattern, page)
        return items

    # form list urls
    def listUrl(self):
        indexPage = self.getPage(1)
        listurls = []
        if indexPage is not None:
            print "indexpage is valid\ngetting listurls:"
            pageNum = self.getPageNum(indexPage)
            for n in range(1,2):
                page = self.getPage(n)
                listurl = self.getTitle(page)
                listurls.extend(listurl)
                print "complete page " + str(n)
            print "complete all thread titles in the first page"
            return listurls
        else:
            return None


# Thread
class THREAD:
    # initialization
    def __init__(self, baseUrl):
        self.baseURL = baseUrl
        self.tool = Tool()
        self.file = None

    # get thread page
    def getPage(self, pageNum):
        try:
            url = 'https://forums.tesla.com/forum/forums/' + self.baseURL + '?page=' + str(pageNum-1)
            '''request = urllib2.Request(url)
            request.add_header('Accept-encoding', 'gzip')
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
            request.add_header('Host', 'teslamotorsclub.com')
            request.add_header('Referer',
                               'https://teslamotorsclub.com/tmc/forums/model-s-ordering-production-delivery.112/')
            request.add_header('GET', url)'''
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            response = opener.open(url)
            content = response.read()
            gzipped = response.headers.get('Content-Encoding')
            if gzipped:
                content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
            return content
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"Connection Failed", e.reason
                return None

    # get total pageNum
    def getPageNum(self, page):
        pattern = re.compile('pager-last.*?><.*?page=(.*?)">', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return 1

    # get thread content
    def getContent(self,page):
        pattern = re.compile('encoded">(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        print "The content is here\n"
        for item in items:
            content = self.tool.replace(item)+'\n'
            contents.append(content)
            print "This is content only"
            print content      # here is the content   we can use the content here
            print "This is contents only"
            #print contents
            #print
            # print "Content is here\n" + content
        return contents        # what is contents for here?

    # NLP process
    def nlp(self, posts, al):
        results = al.keywords(text=posts, sentiment=True)
        keywords = results['keywords']
        print "This is the keywords and sentiment analysis"
        for keyword in keywords:
            #print "Notation A"
            print keyword['text']+ "," +keyword['sentiment']['type']
            #print keyword['sentiment']['type']


    # main function
    def main(self):
        print "Thread Title: " + self.baseURL + "\n"
        alchemy_language = AlchemyLanguageV1(api_key='ca6e6bb5f8997ce199be500d6b1c79e1f0158bc8')
        indexPage = self.getPage(1)
        if indexPage is not None:
            pageNum = self.getPageNum(indexPage)
            posts = []
            for n in range(1,int(pageNum)+1):    # here n is the page number
                page = self.getPage(n)           # use getPage method to get the pages
                post = self.getContent(page)    # use getContent method (page) variable
                posts.extend(post)
            print "Complete Collecting Content\n"
            print "page notation"
            #self.getContent(self,page)
            self.nlp(posts, alchemy_language)    #use nlp method
        else:
            return None

def main():
    time.sleep(1)
    baseURL = 'https://forums.tesla.com/forum/tesla-model-s'
    list = LIST(baseURL)         # use the class LIST
    listurls = list.listUrl()    # class LIST(list) listurl method
    print "This is listurls"     # add the notation
    print listurls
    for listurl in listurls:
        thread = THREAD(listurl) #class thread and use the listurl variable
        thread.main()            #what is this for? class thread, main() method

if __name__ == '__main__':    #This is necessary to use the main() function  其他文件调用这个文件的函数时候时，直接Import就可以输出这个函数;这个语句前和语句后的内容都会运行
    main()

print"This is the end"





