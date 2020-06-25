# -*- coding: utf8 -*-
"""
    Базовый скрипт для сбора информации с сайтов auto.ru и др
    Автор: Скворцов Михаил
    e-mail: m.b.skvortz@gmail.com
    Поток: DST-8
    Дата: 27.05.2020

"""
from auto_r_parser import AutoruParser  # Библиотека для разбора сайта auto.ru
import getopt  # Библиотека для обработки входного набора опций
import sys  # Функции для получения входного набора параметров
import pandas as pd  # Статистическая обработка и хранение собранной информации


def getopts():
    """
    :return: список значений входных параметров
    """
    return getopt.getopt(sys.argv[1:], 'o:')


def main():
    """
    Набор входных параметров:
        -o <file_name> файл, куда сохраняется собранная информация
    :return:
    """
    opts = getopts()
    autoru = AutoruParser(_pages=100)
    cars = pd.DataFrame(columns=['brand', 'name', 'modelDate', 'color', 'productionDate', 'bodyType',
                                 'fuelType', 'numberOfDoors', 'vehicleConfiguration', 'vehicleTransmission',
                                 'engineDisplacement', 'whilleType', 'drive','enginePower', 'href', 'kmAge', 'place',
                                 'VIN', 'seller', '#owners', 'inUse', 'pts', 'condition',  'tax', 'castoms',
                                 'exchange', 'price', 'priceCurrency'])

    autoru.go_over_by_params(cars)
    #autoru.go_over_json()
    cars.to_csv(opts[0][0][1], sep=';', encoding='utf-8', index=False)


if __name__ == "__main__":
    main()
