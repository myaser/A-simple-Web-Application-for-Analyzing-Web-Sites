import httplib
import urllib2
from HTMLParser import HTMLParser
from urllib2 import URLError
from urlparse import urlparse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest


class DocTypeParser(HTMLParser):
    version = "UNKNOWN"

    def handle_decl(self, data):
        """
        detects the version of HTML, based on these common declarations:
        https://www.w3schools.com/TAGS/tag_doctype.asp
        uncommon or non standard declarations are not handled, also no declaration is not handled
        """
        data = data.lower()
        if data == "doctype html":
            self.version = "HTML5"
        elif 'html4' in data:
            self.version = "HTML4"
        elif 'xhtml1' in data:
            self.version = "XHTML1"


class AnalyzerSpider(scrapy.Spider):
    name = "analyzer"

    def modify_realtime_request(self, request):
        return SplashRequest(request.url, self.parse,
                             args={
                                 'wait': 0.5,
                             },
                             endpoint='render.html'
                             )

    def _has_login_form(self, response):
        """
        assumption login form contains a single password field and signup contains 2
        """
        forms = response.css('form')
        for form in forms:
            num_passwords = len(form.css('input[type="password"]'))
            if num_passwords == 1:
                return True
        return False

    def _count_inaccessible_links(self, urls):
        """
        assumption will not follow redirects
        use head requests for performance
        """
        bad_links = 0
        for url in urls:
            request = urllib2.Request(url)
            request.get_method = lambda: 'HEAD'
            try:
                response = urllib2.urlopen(request)
                if response.code >= 400:
                    bad_links += 1
            except URLError:
                bad_links += 1
        return bad_links


    def parse(self, response):
        doctype_parser = DocTypeParser()
        doctype_parser.feed(response.text)
        hostname = urlparse(response.url).netloc
        internal_links = LinkExtractor(allow_domains=hostname).extract_links(response)
        external_links = LinkExtractor(deny_domains=hostname).extract_links(response)
        urls = list(map(lambda link: link.url, internal_links)) + \
               list(map(lambda link: link.url, external_links))
        inaccessible_links = self._count_inaccessible_links(urls)
        yield {
            "_status": response.status,
            "version": doctype_parser.version,
            "title": response.xpath('//title/text()').get(),
            "h1": len(response.css('h1').extract()),
            "h2": len(response.css('h2').extract()),
            "h3": len(response.css('h3').extract()),
            "h4": len(response.css('h4').extract()),
            "h5": len(response.css('h5').extract()),
            "h6": len(response.css('h6').extract()),
            "internal_links": len(internal_links),
            "external_links": len(external_links),
            "inaccessible_links": inaccessible_links,
            "login-form": self._has_login_form(response),
        }
