import scrapy
from realestate.items import RealestateItem  # Adjust this import based on your project structure

class HepsiemlakSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["hepsiemlak.com"]
    start_urls = [
        'https://www.hepsiemlak.com/sisli-kiralik'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # Find all listing items
        listings = response.css('ul.list-items-container li.listing-item')
        counter = 0
        # Loop through each listing item
        for listing in listings:
            # Create an instance of RealestateItem
            if(counter == 10):
                break
            item = RealestateItem()

            # Populate item fields
            item['id'] = listing.css('article::attr(id)').get('').strip()
            item['title'] = listing.css('h3::text').get('').strip()
            item['price'] = listing.css('.list-view-price::text').get('').strip()
            item['currency'] = listing.css('.currency::text').get('').strip()
            item['location'] = listing.css('div.list-view-location > span:last-child::text').get().strip()
            item['property_type'] = listing.css('.short-property .left::text').get('').strip()
            item['rooms'] = listing.css('.houseRoomCount::text').get('').strip()
            item['size'] = listing.css('.list-view-size::text').get('').strip()
            item['age'] = listing.css('.buildingAge::text').get('').strip()
            item['floor'] = listing.css('.floortype::text').get('').strip()
            item['date'] = listing.css('.list-view-date::text').get('').strip()
            item['image_url'] = listing.css('.img-link-picture img::attr(src)').get('').strip()
            item['agency_logo'] = listing.css('.branded img::attr(src)').get('').strip()

            # Yield the item
            yield item

        # Follow pagination link if it exists
        next_page = response.css('a.he-pagination__navigate-text--next::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), self.parse)
