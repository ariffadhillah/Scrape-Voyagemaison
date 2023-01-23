import requests
from requests_html import HTMLSession
import pandas as pd
import time


# url ='https://www.voyagemaison.com/collections/cushions'
s = HTMLSession()

cushionlist  = []

def request(url):

    r = s.get(url)

    # r.html.render(sleep=1)

    return r.html.xpath('//*[@id="shopify-section-template--16567270998259__main"]/div[1]/div[3]/ul', first=True)

def parse(products):
    for item in products.absolute_links:
        r = s.get(item)
        name = r.html.find('h1.product-title', first=True).text
        try:
            rating = r.html.find('span.ruk-rating-snippet-count', first=True).text
        except:
            rating = 'no ranting'   
        price = r.html.find('div.cd.price__current', first=True).text
        description = r.html.find('div.product-description.rte', first=True).text
        specification = r.html.find('#content-specification', first=True).text
        delivery = r.html.find('div.product-delivery.rte', first=True).text

        cushion = {
            'name': name,
            'ranting': rating,
            'price': price,
            'description' : description,
            'specification' : specification,
            'delivery' : delivery
        }

        cushionlist.append(cushion)

def output():
    df = pd.DataFrame(cushionlist)
    df.to_csv('cushionlist.csv')
    print('Save to CSV file')

x=1
while True:
    try:
        products = request(f'https://www.voyagemaison.com/collections/cushions?page={x}')
        print(f'Getting items from page {x}')
        parse(products)
        print('total Items: ', len(cushionlist))
        x=x+1
        time.sleep(2)
    except:
        print('No more items!')
        break

output()
