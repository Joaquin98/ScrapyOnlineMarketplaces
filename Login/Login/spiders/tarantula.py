import scrapy
from scrapy.http import FormRequest

class TarantulaSpider(scrapy.Spider):
    name = 'tarantula'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/basic_login_check/']

    def start_requests(self):
        login_url = 'https://scrapingclub.com/exercise/basic_login/'
        yield scrapy.Request(login_url, callback=self.login,
                       headers={"User-Agent": "My UserAgent"},
                       meta={"proxy": "http://200.0.247.86:4153"})

    def login(self,response):
        token = response.css('input[name="csrfmiddlewaretoken"]::attr(value)').extract_first()
        yield FormRequest.from_response(response,
                            formdata={'csrfmiddlewaretoken':token,'name': 'scrapingclub', 'password': 'scrapingclub'},
                            callback=self.parse)

    def parse(self, response):
        text = response.css('div.mt-4>p').get()
        yield {'text' : text}
