from turtle import title
import scrapy

#titulo = //h1/a/text()
#citas = //span[@class="text" and @itemprop="text"]/text()
#Top ten = //div[@contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
#next_page=  response.xpath('//ul[@class = "pager"]//li[@class="next"]/a/@href').get()
class QuotesSpider(scrapy.Spider):
    name= 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response): #Analizar la respuesta http y a partir de eso regresar lo que necesitamos
        title = response.xpath('//h1/a/text()').get()
        #print(f'Title: {title}')

        quotes= response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        #print('Citas: ')
        #for quote in quotes:
        #    print(f'- {quote}')
        #print('\n\n')
        top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        #print('Tags: ')
        #for tag in top_ten_tags:
        #   print(f'- {tag}')
        #print(response.status, response.headers)
        
        #retorno parcial de los datos
        yield{
            'title': title,
            'quotes': quotes,
            'top ten tags': top_ten_tags
        }

        next_page_button_link =  response.xpath('//ul[@class = "pager"]//li[@class="next"]/a/@href').get()

        if next_page_button_link:
            yield response.follow(next_page_button_link)
        #para mandar a un archivo:  scrapy crawl quotes -o quotes.csv
        #para no sobreescribir : rm quotes.json && scrapy crawl quotes -o quotes.json
