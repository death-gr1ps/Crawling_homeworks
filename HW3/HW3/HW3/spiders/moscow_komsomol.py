from ..items import MkItem
import scrapy
from scrapy_playwright.page import PageMethod

DELAY = 5000

class MoscowKomsomolSpider(scrapy.Spider):
    name = "moscow_komsomol"
    allowed_domains = ["mk.ru"]
    start_urls = "https://www.mk.ru/sitemap/articles_sitemap_10_map.xml"
    custom_settings = {
        'DOWNLOAD_HANDLERS': { 
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }

    cond_dict = {"playwright": True, 'playwright_include_page': True,
                 "playwright_page_methods": [PageMethod('wait_for_timeout', DELAY)]}


    def start_requests(self):
        """Start by fetching the sitemap."""
        yield scrapy.Request(url=self.start_urls, callback=self.parse_sitemap, meta=self.cond_dict)

    async def parse_sitemap(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        """Parse the sitemap to get brand URLs."""
        # Extracting all brand URLs from the sitemap
        news_urls = response.xpath("//url/loc/text()").getall()

        # Yielding requests for each brand URL
        for url in news_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta=self.cond_dict)
 
    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        title                = response.xpath("//h1/text()").get()
        description          = response.xpath('//meta[@name="description"]/@content').get()
        article_text         = response.xpath("///div[@class='article__body']/p/text()").getall()
        publication_datetime = response.xpath("//meta[@itemprop='datePublished']/@content").get()
        header_photo_url     = response.xpath("//img[@class='article__picture-image']/@src").get()
        keywords             = response.xpath("//meta[@name='keywords']/@content").get()
        authors              = response.xpath("//div[@class='article__authors-data']//meta[@itemprop='name']/@content").getall()

        if self.valid_field(title) and self.valid_field(description) and self.valid_field(article_text) and self.valid_field(publication_datetime) and\
            self.valid_field(keywords) and self.valid_field(authors) and self.valid_field(response.url):
            yield MkItem(
                title                = self.to_str(title),
                description          = self.to_str(description),
                article_text         = self.to_str(article_text),
                publication_datetime = self.to_str(publication_datetime),
                header_photo_url     = self.to_str(header_photo_url),
                keywords             = self.to_str(keywords),
                authors              = self.to_str(authors),
                source_url           = self.to_str(response.url)
            )

    def to_str(self, string):
        if string != None:
            return string.strip()
        
    def valid_field(self, val) ->bool:
        return val not in {None, ""}