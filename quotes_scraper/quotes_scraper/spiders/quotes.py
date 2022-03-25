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

    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS':24, #numero de peticiones a la vez
        'MEMUSAGE_LIMIT_MB': 2048, #cuanta memoria ram queremos que use
        'MEMUSAGE_NOTIFY_MAIL':  ['betydiscretas@gmail.com'], #aviso de uso de memoria
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'BETTY SANCHEZ', #quien hizo la petición,
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes= kwargs['quotes']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        next_page_button_link =  response.xpath('//ul[@class = "pager"]//li[@class="next"]/a/@href').get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes})
        else:
            yield{
                'quotes':quotes
            }
    def parse(self, response): #Analizar la respuesta http y a partir de eso regresar lo que necesitamos
        title = response.xpath('//h1/a/text()').get()
        #print(f'Title: {title}')

        quotes= response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        #print('Citas: ')
        #for quote in quotes:
        #    print(f'- {quote}')
        #print('\n\n')
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        #print('Tags: ')
        #for tag in top_ten_tags:
        #   print(f'- {tag}')
        #print(response.status, response.headers)
        
        top = getattr(self, 'top', None)
        #scrapy crawl quotes -a top=3
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        #retorno parcial de los datos
        yield{
            'title': title,
            'top ten tags': top_tags
        }

        next_page_button_link =  response.xpath('//ul[@class = "pager"]//li[@class="next"]/a/@href').get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes})
        #para mandar a un archivo:  scrapy crawl quotes -o quotes.csv
        #para no sobreescribir : rm quotes.json && scrapy crawl quotes -o quotes.json
