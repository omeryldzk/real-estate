import scrapy
from scrapy_splash import SplashRequest

class HepsiemlakSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["hepsiemlak.com"]
    start_urls = [
        'https://www.hepsiemlak.com/sisli-kiralik'
    ]

    # Lua script for Splash to wait for JavaScript to render
    lua_script = """
    function main(splash, args)
        splash:go(args.url)
        splash:wait(5)  -- Adjust wait time as needed
        return splash:html()
    end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='render.html', args={'lua_source': self.lua_script})

    def parse(self, response):
    # Find all listing items
        listings = response.css('ul.list-items-container li.listing-item')

        # Loop through each listing item
        for listing in listings:
            yield {
                'id': listing.css('article::attr(id)').get('').strip(),
                'title': listing.css('h3::text').get('').strip(),
                'price': listing.css('.list-view-price::text').get('').strip(),
                'currency': listing.css('.currency::text').get('').strip(),
                'location': listing.css('.list-view-location::text').get('').strip(),
                'property_type': listing.css('.short-property .left::text').get('').strip(),
                'rooms': listing.css('.houseRoomCount::text').get('').strip(),
                'size': listing.css('.list-view-size::text').get('').strip(),
                'age': listing.css('.buildingAge::text').get('').strip(),
                'floor': listing.css('.floortype::text').get('').strip(),
                'date': listing.css('.list-view-date::text').get('').strip(),
                'image_url': listing.css('.img-link-picture img::attr(src)').get('').strip(),
                'agency_logo': listing.css('.branded img::attr(src)').get('').strip(),
            }


        # Follow pagination link if it exists
        next_page = response.css('a.he-pagination__navigate-text--next::attr(href)').get()
        if next_page:
            yield SplashRequest(response.urljoin(next_page), self.parse, endpoint='render.html', args={'lua_source': self.lua_script})
