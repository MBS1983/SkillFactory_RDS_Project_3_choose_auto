# -*- coding: utf8 -*-
"""
    Скрипт для сбора информации с сайта auto.ru
    Автор: Скворцов Михаил
    e-mail: m.b.skvortz@gmail.com
    Поток: DST-8
    Дата: 28.05.2020

"""
from bs4 import BeautifulSoup
import requests  # Библиотека для формирования и отправки html-запросов

headers = '''
Host: auto.ru
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: */*
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://auto.ru/perm/cars/all/
x-client-app-version: 201911.26.155818
x-csrf-token: a5446446051b69f4b14cb18507b6ebb9954c6cf76b93027f
x-requested-with: fetch
content-type: application/json
Origin: https://auto.ru/ufa/
Content-Length: 157
DNT: 1
Connection: keep-alive
Cookie: _csrf_token=a5446446051b69f4b14cb18507b6ebb9954c6cf76b93027f; autoru_sid=a%3Ag5dde33da257four8ct4hhlt0a17h00o.5bc9aa797010bf795c3fae4e20dd2eef%7C1574843354139.604800.PHszmA0eR_XZhCgieItl5g.WeKyrJqm5x5NmWaOBK-TLSEyI0wo2Z27miqpLLFwee8; autoruuid=g5dde33da257four8ct4hhlt0a17h00o.5bc9aa797010bf795c3fae4e20dd2eef; suid=d6c67bcdfb90c719a1008ae312af2fc9.f9f984e280d08277d997ce0fac3c604c; from_lifetime=1574843440313; from=google-search; counter_ga_all7=1; X-Vertis-DC=sas; navigation_promo_seen-recalls=true
Pragma: no-cache
Cache-Control: no-cache
'''.strip().split("\n")

url = "https://auto.ru/ufa/-/ajax/desktop/listing/"
#'moskovskaya_oblast', 'ufa','kazan','rossiya', 'sankt-peterburg', 'tyva', 'tverskaya_oblast', 'vladimir',
#          'volgograd', 'voronezh','ekaterinburg','ivanovo', 'kaluga', 'kostroma', 'krasnodar', 'krasnoyarsk',
#            'nizhniy_novgorod','novosibirsk', 'omsk', 'perm',
cities = [ 'rostov-na-donu', 'samara', 'saratov', 'tula',
          'chelyabinsk', 'moskva', 'yaroslavl']


def create_query(_city='moskva', _year_from=0, _year_to=0, _km_age_from=0,
                 _km_age_to=0, _page=1):
    """
    Функция генерирует строку запроса в соответствии с заданными параметрами\n
    :param _city:
    :param _year_from:
    :param _year_to:
    :param _km_age_from:
    :param _km_age_to:
    :param _page:
    :return: url
    """
    url = "https://auto.ru/" + _city + "/cars/all/?sort=fresh_relevance_1-desc"
    if _year_from != 0:
        url += "&year_from=" + str(_year_from)

    if _year_to != 0:
        url += "&year_to=" + str(_year_to)

    if _km_age_from != 0:
        url += "&km_age_from=" + str(_km_age_from)

    if _km_age_to != 0:
        url += "&km_age_to=" + str(_km_age_to)

    url += "&page=" + str(_page) + "&output_type=list"
    return url


def get_page_by_url(_url):
    """
    Функция по url возвращает запрошенную страницу\n
    :param _url: адрес страницы
    :return: структура responce из библиотеки requests
    """

    return requests.get(_url)

def get_page_by_url_json(_url, _dict_headers, _city, _page):
    param = {
        "url": create_query(_city,_page=_page),
        "region":_city,
        "section": "all",
        "category": "cars",
        "sort": "fresh_relevance_1-desc",
        "page": _page
    }
    response = requests.post("https://auto.ru/ufa/", json=param, headers = _dict_headers)#_url
    data = response.json()  # Переменная data хранит полученные объявления
    return data


def print_content(_buf, _file="d:\\skillfactory\\Real Data Science\\4.Auto_pickup\\auto_resp_content.txt"):
    """
    Отладочная функция, выводит содержимое _buf в тестовый файл\n
    :param _file:
    :param _buf: выводимый буфер
    :return:
    """
    out_file = open(_file, 'w', encoding='utf-8')
    out_file.write(_buf)
    out_file.close()


def pars_item(_cars, _item, _owner):
    """
    Функция разбирает конкртеное объявление\n
    :param _owner: часть данных с описанием характеристик владельца
    :param _cars: датафрейм куда разбираются выделенные объявления
    :param _item: объявление выделенное с исходной страницы
    :return:
    """
    seller = _owner.find('a', class_='Link ListingItemSalonName-module__container ListingItem-module__salonName')

    if seller is None:
        seller = 'Private'
    else:
        seller = seller.text

    car_info = {'brand': _item.find('meta', itemprop='brand').attrs['content'],
                'name': _item.find('meta', itemprop='name').attrs['content'],
                'modelDate': _item.find('meta', itemprop='modelDate').attrs['content'],
                'color': _item.find('meta', itemprop='color').attrs['content'],
                'productionDate': _item.find('meta', itemprop='productionDate').attrs['content'],
                'bodyType': _item.find('meta', itemprop='bodyType').attrs['content'],
                'fuelType': _item.find('meta', itemprop='fuelType').attrs['content'],
                'numberOfDoors': _item.find('meta', itemprop='numberOfDoors').attrs['content'],
                'vehicleConfiguration': _item.find('meta', itemprop='vehicleConfiguration').attrs['content'],
                'vehicleTransmission': _item.find('meta', itemprop='vehicleTransmission').attrs['content'],
                'engineDisplacement': _item.find_next('meta', itemprop='engineDisplacement').attrs['content'],
                'whilleType': '',
                'drive': '',
                'enginePower': _item.find_next('meta', itemprop='enginePower').attrs['content'],
                'href': _item.find_next('meta', itemprop='url').attrs['content'],
                'kmAge': _owner.find('div', class_=u'ListingItem-module__kmAge').text,
                'place': '',
                'VIN': '',
                'seller': seller,
                '#owners': 0,
                'inUse': 0,
                'pts': '',
                'condition': '',
                'price': _item.find_next('meta', itemprop='price').attrs['content'],
                'tax': 0,
                'castoms': '',
                'exchange': '',
                'priceCurrency': _item.find_next('meta', itemprop='priceCurrency').attrs['content']
                }
    href = car_info['href']
    page_auto = get_page_by_url(href)
    full_page = BeautifulSoup(page_auto.text.encode(page_auto.encoding), 'html.parser')

    loc = _owner.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp')
    if loc != None:
        car_info['place'] = loc.text

    if car_info['kmAge'] != 'Новый':
        full_params = full_page.find_all('span', class_='CardInfo__cell')
        tag_perv = full_params[0]
        for tag in full_params:
            if tag_perv.text == 'Налог':
                car_info['tax'] = tag.text

            if tag_perv.text == 'Привод':
                car_info['drive'] = tag.text

            if tag_perv.text == 'Руль':
                car_info['whilleType'] = tag.text

            if tag_perv.text == 'Владельцы':
                car_info['#owners'] = tag.text

            if tag_perv.text == 'ПТС':
                car_info['pts'] = tag.text

            if tag_perv.text == 'Владение':
                car_info['inUse'] = tag.text

            if tag_perv.text == 'Таможня':
                car_info['castoms'] = tag.text

            if tag_perv.text == 'Обмен':
                car_info['exchange'] = tag.text

            if tag_perv.text == 'Состояние':
                car_info['condition'] = tag.text

            if tag_perv.text == 'VIN':
                car_info['VIN'] = tag.text

            tag_perv = tag
    else:
        main_params = full_page.find_all('div', class_='CardInfoGrouped__cellValue')
        if len(main_params)>3:
            car_info['tax'] = main_params[1].text
            car_info['drive'] = main_params[3].text

    _cars.loc[len(_cars)] = car_info
    pass


def pars_page(_cars, _page):
    """
    Функция разбирает конкретную страницу сайта\n
    :param _cars: датафрейм куда разбираются выделенные объявления
    :param _page: Данные сайта
    :return:
    """
    root = BeautifulSoup(_page, 'html.parser')

    # Находим список объявлений на странице
    # Почемуто не удалось выделить общий контейнер поэтому owner и items две составные части общего
    owner = root.find_all('div', class_='ListingItem-module__main')
    items = root.find_all('span', itemtype="http://schema.org/Car")

    for index in range(len(items)):
        pars_item(_cars, items[index], owner[index])
        pass


class AutoruParser:
    def __init__(self, _pages=100):
        """
        Класс инициализируется количеством страниц, которые пробегаются\n
        :param _pages:
        """
        self.pages = _pages
        self.url = "https://auto.ru/ufa/-/ajax/desktop/listing/"
        self.dict_headers = {}
        for header in headers:
            key, value = header.split(': ')
            self.dict_headers[key] = value

    def go_over_by_params(self, _cars, _city='moskva', _year_from=0, _year_to=0, _km_age_from=0,
                          _km_age_to=0):
        """
        Функция получает страницы одна за другой, удовлетвоярющие набору параметров, поступающих из вне,
        выделяет из них объявления и сохраняет  датафрейм\n
        :param _cars: датафрейм куда разбираются выделенные объявления
        :param _city: город в котором тищутся объявления
        :param _year_from: минимальный год выпуска
        :param _year_to: максимальный год выпуска
        :param _km_age_from: минимальный пробег
        :param _km_age_to: максимальный пробег
        :return: dataframe
        """

        for city in cities:
            print("Process {}".format(city))
            for i in range(1, self.pages):
                url = create_query(city, _year_from, _year_to, _km_age_from, _km_age_to, _page=i)
                page = get_page_by_url(url)
                pars_page(_cars, page.text.encode(page.encoding))

            _cars.to_csv("d:\\skillfactory\\Real Data Science\\4.Auto_pickup\\auto_bd.csv", sep=';', encoding='utf-8',
                         index=False)

    def go_over_json(self):
        for city in cities:
            print("Process {}".format(city))
            for i in range(1, self.pages):
                #url = create_query(city, _page=i)
                page = get_page_by_url_json(self.url, self.dict_headers, 'ufa', i)
                pass
               # pars_page(_cars, page.text.encode(page.encoding))

