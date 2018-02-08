from bs4 import BeautifulSoup
import requests
import re
import time


def resolve_single_page(url, data):
    headers = {
        "User - Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    _title = soup.find('p', {"class": "title_p"})
    _price = soup.find('span', {"class": "jiage"})
    _lcsp = soup.find('div', {"class": "lcsp_info"})

    title = _title.get_text()
    price = _price.get_text()
    lcsp = _lcsp.get_text()
    print(title, price, lcsp, sep="\n")
    data.write(title + '\n' + price + '\n' + lcsp)
    data.write("\n---------------------------------------------\n")


def get_items(url):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    # _urls = soup.find('div',{"class":"col col2"}).find('a')
    _urls = soup.find_all('div', {"class": "col col2"})
    urls = []
    for x in _urls:
        link = x.find('a').get('href')
        if link:
            urls.append(link)
    print(urls)
    return urls


def page_get_items(url, data):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    #    titles = soup.select('h1[class="info_tit"]').text
    titles = soup.find_all('h1', {"class": "info_tit"})
    info_params = soup.find_all('div', {"class": "info_param"})
    prices = soup.find_all('div', {"class": "col col3"})
    for title, info_param, price in zip(titles, info_params, prices):
        title_string = "商品名称：" + title.text.strip() + '\n'

        param_strings = info_param.text.split()
        print(param_strings)
        gongli_string = "公里数:" + param_strings[0] + '\n'
        rongliang_string = "容量:" + param_strings[1] + '\n'
        fangshi_string = "自动/手动:" + param_strings[2] + '\n'

        price_string = "\n价格：" + price.find('h3').text
        sep_string = "\n------------------------\n"
        print(title_string, gongli_string, rongliang_string, fangshi_string, price_string, sep_string)
        data.write(title_string + gongli_string + rongliang_string + fangshi_string + price_string + sep_string)


def get_pages(url, i):
    urls = []
    for a in range(i):
        urls.append(url + '/pn' + str(i))
    return urls


with open("data.txt", 'w') as data:
    url = "http://sh.58.com/ershouche"
    urls = get_pages(url, 50)
    print(urls)
    i = 0
    for x in urls:
        page_get_items(x, data)
        time.sleep(1)
        '''
        y = get_items(x)
        for temp in y:
            resolve_single_page(temp, data)
            time.sleep(3)
            i = i + 1
            print("\n------------------------------------\n", i)
            '''
    data.close()
