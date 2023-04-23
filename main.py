import requests, lxml, json, time
from bs4 import BeautifulSoup
import re

cookies = {
    'mage-banners-cache-storage': '%7B%7D',
    'PHPSESSID': 'l4mjvbggtp6ut75bg9n35hq7uq',
    'countryselector_geoip_last_resolved_store': '{"store_code":"bahco_ru_ru","frontend_label":"\\u0420\\u043e\\u0441\\u0441\\u0438\\u044f \\/ \\u0420\\u0443\\u0441\\u0441\\u043a\\u0438\\u0439","store_base_url":"https:\\/\\/www.bahco.com\\/ru_ru\\/"}',
    'countryselector_preferred_store': 'https://www.bahco.com/ru_ru/',
    '_mkto_trk': 'id:787-KJR-916&token:_mch-bahco.com-1679779495907-21022',
    'form_key': 'U8LdOcljywLLRIM6',
    'form_key': 'U8LdOcljywLLRIM6',
    '_gcl_au': '1.1.1991172558.1679779497',
    'mage-messages': '',
    'ln_or': 'eyIxNzQzNDU3LDI1MDEwMDIiOiJkIn0%3D',
    'OptanonAlertBoxClosed': '2023-03-25T21:25:01.994Z',
    '_ga': 'GA1.2.877999552.1679779516',
    '_gid': 'GA1.2.589294301.1679779516',
    'X-Magento-Vary': 'b8017c883354ce24bb00e72d165aaf417ec8bf32',
    'mage-cache-storage': '%7B%7D',
    'mage-cache-storage-section-invalidation': '%7B%7D',
    'mage-cache-sessid': 'true',
    'recently_viewed_product': '%7B%7D',
    'recently_viewed_product_previous': '%7B%7D',
    'recently_compared_product': '%7B%7D',
    'recently_compared_product_previous': '%7B%7D',
    'product_data_storage': '%7B%7D',
    '_gat_UA-23872204-2': '1',
    'private_content_version': 'd0a4739dbf3888a6820ea43a0d1b10e2',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Sun+Mar+26+2023+02%3A36%3A04+GMT%2B0300+(%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.33.0&isIABGlobal=false&hosts=&consentId=a37c82dc-a4d1-4020-b922-aed6b73d6d0c&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=RU%3BSPE&AwaitingReconsent=false',
    'section_data_ids': '%7B%7D',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'mage-banners-cache-storage=%7B%7D; PHPSESSID=l4mjvbggtp6ut75bg9n35hq7uq; countryselector_geoip_last_resolved_store={"store_code":"bahco_ru_ru","frontend_label":"\\u0420\\u043e\\u0441\\u0441\\u0438\\u044f \\/ \\u0420\\u0443\\u0441\\u0441\\u043a\\u0438\\u0439","store_base_url":"https:\\/\\/www.bahco.com\\/ru_ru\\/"}; countryselector_preferred_store=https://www.bahco.com/ru_ru/; _mkto_trk=id:787-KJR-916&token:_mch-bahco.com-1679779495907-21022; form_key=U8LdOcljywLLRIM6; form_key=U8LdOcljywLLRIM6; _gcl_au=1.1.1991172558.1679779497; mage-messages=; ln_or=eyIxNzQzNDU3LDI1MDEwMDIiOiJkIn0%3D; OptanonAlertBoxClosed=2023-03-25T21:25:01.994Z; _ga=GA1.2.877999552.1679779516; _gid=GA1.2.589294301.1679779516; X-Magento-Vary=b8017c883354ce24bb00e72d165aaf417ec8bf32; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; _gat_UA-23872204-2=1; private_content_version=d0a4739dbf3888a6820ea43a0d1b10e2; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Mar+26+2023+02%3A36%3A04+GMT%2B0300+(%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.33.0&isIABGlobal=false&hosts=&consentId=a37c82dc-a4d1-4020-b922-aed6b73d6d0c&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=RU%3BSPE&AwaitingReconsent=false; section_data_ids=%7B%7D',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

url = 'https://www.bahco.com/ru_ru/produkcija.html'
all_data = []

def get_start_links(url):
    links = []
    response = requests.get(url=url, cookies=cookies, headers=headers)
    src = response.text
    soup = BeautifulSoup(src, 'lxml')
    print(url)
    try:
        lis = soup.find('div', class_='column main').find_all('li', class_='category-item')[1:]
        for li in lis:
            href = li.get('data-url')
            links.append(href)
        links.append('https://www.bahco.com/ru_ru/nabor-instrumenta-v-futljare--17-sht-pb_9852_.html')
        links.append('https://www.bahco.com/ru_ru/nabor-instrumenta-v-futljare--7-sht-pb_9841_.html')
        links.append('https://www.bahco.com/ru_ru/nabor-instrumenta-v-futljare--7-sht-pb_9848_.html')
        return links
    except:
        print('Ошибка')

def get_page_links(link):
    try:
        response = requests.get(url=link, cookies=cookies, headers=headers)
    except:
        print('Ошибка ', link)
        return
    print(link)
    src = response.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        links = []
        lis = soup.find('div', class_='column main').find_all('li', class_='category-item')[1:]
        for li in lis:
            href = li.get('data-url')
            links.append(href)
    except:
        links = None

    if not links:
        try:
            script = soup.find('div', class_='products wrapper grid products-grid').find('script').text
            data = script.split('var data = ')[1].split('];')[0].split('},')
            for frame in data:
                try:
                    url = frame.split('url:')[1].split(',')[0].lstrip(" '").rstrip("'")
                    print(url)
                    print(f'Хочу собрать данные с {url}')
                    data = get_card_data(url)
                    all_data.append(data)
                except:
                    continue
        except:
            print('Ошибка')

    else:
        print('Нашел еще ссылки')
        for link in links:
            print('Иду в ', link)
            get_page_links(link)

def get_card_data(url):
    response = requests.get(url=url, cookies=cookies, headers=headers)
    src = response.text
    soup = BeautifulSoup(src, 'lxml')
    top = soup.find('div', class_='page-title-wrapper product')
    title = top.find('h1').get_text()
    article = top.find('div', class_='value').get_text()
    table = soup.find('div', class_='data item technical-details').find('table')
    head = table.find('thead').find_all('th')[1:-1]
    body = table.find('tbody').find_all('tr')
    chars = []
    chars.append('Товар')
    for t in head:
        # print(t)
        text = t.find('img').get('title')
        if text not in chars:
            chars.append(text)
        else:
            text = text + '_2'
            chars.append(text)
    # print(chars)
    data = []
    for tr in body:
        tds = tr.find_all('td')[:-1]
        values = []
        for td in tds:
            value = td.get_text().replace('\n', '')
            values.append(value)
        line = dict(zip(chars, values))
        data.append(line)
        # print(line)
    # print(data)
    data_card = {}
    data_card['Наименование товара'] = title
    data_card['Артикул'] = article
    data_card['Характеристики'] = data
    try:
        extra_data = soup.find('div', class_='data item set-content')
    except Exception:
        extra_data = None
    if extra_data:
        complectation = []
        table = extra_data.find('ol', class_='products list items product-items-secondary product-slider').find_all('li')
        for window in table:
            spans = window.find('div', class_='product details product-item-details').find_all('span')
            extras = []
            for span in spans:
                text = span.get_text()
                extras.append(text)
            extra_card = {'Наименование': extras[0], 'Артикул': extras[1]}
            complectation.append(extra_card)
        # print(complectation)
        data_card['Комплектация'] = complectation
    print(data_card)
    return data_card





def main():
    start = time.time()
    all_links = get_start_links(url)
    print(all_links)
    for link in all_links:
        get_page_links(link)
    with open('data2.json', 'w', encoding="utf-8") as file:
        json.dump(all_data, file, indent=4, ensure_ascii=False)
    finish = time.time()
    work_time = finish-start
    print(work_time)

if __name__ == '__main__':
    main()

