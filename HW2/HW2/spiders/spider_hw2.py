import scrapy
from scrapy.spiders import SitemapSpider
from ..items import BookItem


class ProductsSpider(SitemapSpider):
    name = 'spider_hw2'
    allowed_domains = ['chitai-gorod.ru']
    sitemap_urls = ['https://www.chitai-gorod.ru/sitemap/products6.xml']

    def parse(self, response):
        ''' Extracting data from each page from sitemap url'''
        
        title            = response.xpath('//h1/text()').get()
        author           = response.xpath("""//ul[@class="product-authors"]//a[@class='global-link']/text()""").get() or \
            response.xpath("//li[@class='product-authors__link']//a[@class='global-link']/text()").get()
        description      = response.xpath('//div[@class="product-description-short__text"]/text()').get()
        raw_price        = response.xpath("//span[@class='product-offer-price__actual']/text()").get()
        currency         = self.give_currency(raw_price)
        price_amount     = self.parse_num(raw_price)
        rating_value     = response.xpath('//span[@class="product-rating__votes"]//span[1]/text()').get()
        rating_count_raw = response.xpath('//span[@class="product-rating__votes"]//span[2]/text()').get()
        rating_count     = self.parse_num(rating_count_raw)
        publication_year = response.xpath('//span[@itemprop="datePublished"]/span/text()').get()
        isbn             = response.xpath('//span[@itemprop="isbn"]/span/text()').get()
        pages_cnt        = response.xpath('//span[@itemprop="numberOfPages"]/span/text()').get()
        publisher        = response.xpath('//span[@itemprop="publisher"]/a/text()').get()
        book_cover       = response.xpath('//img[@class="product-preview__placeholder"]/@src').get()

        if self.valid_field(title) and self.valid_field(publication_year) and self.valid_field(isbn) and self.valid_field(pages_cnt) and self.valid_field(response.url):
            yield BookItem(
                title            = self.to_str(title),
                author           = self.to_str(author),
                description      = self.to_str(description),
                price_amount     = self.change_type(self.to_str(price_amount), int),
                price_currency   = currency,
                rating_value     = self.change_type(self.to_str(rating_value), float),
                rating_count     = self.change_type(self.to_str(rating_count), int),
                publication_year = self.change_type(self.to_str(publication_year), int),
                isbn             = self.to_str(isbn),
                pages_cnt        = self.change_type(self.to_str(pages_cnt), int),
                publisher        = self.to_str(publisher),
                book_cover       = self.to_str(book_cover),
                source_url       = self.to_str(response.url)
            )

    def valid_field(self, val) ->bool:
        return val not in {None, ""}
    
    def change_type(self,string, type):
        if string != None:
            return type(string)
    
    def to_str(self, string):
        if string != None:
            return string.strip()
    
    def give_currency(self, val) ->str:
        if isinstance(val, str):
            return val.split()[-1]
        
        return '₽'
    
    def parse_num(self, price_str):
        if price_str == None:
            return None
        
        cleaned_str = ''.join(filter(str.isdigit, price_str))

        if not cleaned_str:
            return None
        
        return cleaned_str

    # scrapy crawl spider_hw2 -o spider_hw2.jsonlines