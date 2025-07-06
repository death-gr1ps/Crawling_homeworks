import scrapy
from ..items import PointItem, OrganizationItem


class SpiderHw1Spider(scrapy.Spider):
    name = "spider_hw1"
    allowed_domains = ["merchantpoint.ru"]
    sitemap_url = "https://merchantpoint.ru/sitemap/brands.xml"

    def start_requests(self):
        """Start by fetching the sitemap."""
        yield scrapy.Request(url=self.sitemap_url, callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        """Parse the sitemap to get brand URLs."""
        # Extracting all brand URLs from the sitemap
        brand_urls = response.xpath("//url/loc/text()").getall()

        # Correcting the URLs
        corrected_urls = [url.replace('/mcc/', '/') for url in brand_urls]

        # Yielding requests for each brand URL
        for url in corrected_urls:
            yield scrapy.Request(url=url, callback=self.parse_org)

    def parse_org(self, response):
        """Collecting info about organization and its merchant points."""
        # Org data
        org_name = response.xpath("//h1/text()").get()
        org_description = response.xpath("//div[@class='form-group mb-2']//p[2]/text()").get()
        source_url = response.url

        # Merchant points data in table
        rows = response.xpath("//table[@class='finance-table']/tbody/tr")
        data = []
        
        # Parsing table
        for row in rows:
            mcc = row.xpath('./td[1]/text()').get()
            tsp = row.xpath('./td[2]/a/text()').get()
            address = row.xpath('./td[3]/text()').get()
            if address is not None:
                address = str(address).strip()
            point_item = PointItem(mcc=mcc, merchant_name=tsp, address=address)
            data.append(point_item)

        # Organizing data points
        organization_item = OrganizationItem(
            org_name=org_name,
            org_description=org_description,
            source_url=source_url,
            points=data
        )

        yield organization_item
