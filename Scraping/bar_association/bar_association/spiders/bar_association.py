import scrapy


class BarAssociationSpider(scrapy.Spider):
    name = "bar_association"
    #allowed_domains = ["*"]
    start_urls = ["https://www.nmcourts.gov"]

    def parse(self, response):
    
        NEXT_PAGE_SELECTOR = "a::attr(href)"  # the html container for the next page arrow

        next_page = response.css(NEXT_PAGE_SELECTOR).get()
        title = response.css("title::text").get()
        #replace all special characters in title
        title = title.replace(" ", "_")
        title = title.replace("|", "")

        with open("./Results/test.txt", "w") as f:
            f.write(next_page)

        # write response to file
        with open(f"./Results/{title}.txt", "w") as f:
            f.write(response.text)

        

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
