import csv
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


# Объявление класса SaleInfo
class SaleInfo:
    # Определение конструктора класса
    def __init__(self, date, product, category, quantity, price, sum):
        # Присвоение атрибутам класса входных значений
        self.date = datetime.strptime(date, "%Y-%m-%d").date()  # Преобразование входной строки date в тип
        # datetime.date
        self.product = product
        self.category = category
        self.quantity = float(quantity)  # Преобразование количества во float
        self.price = price
        self.sum = float(sum)  # Преобразование суммы во float

    # Определение метода для печати информации, используемого при использовании функции print()
    def __str__(self):
        # Возвращение отформатированной строки, содержащей информацию о продаже
        return f"Sale: {self.date}, {self.product}, {self.category}, {self.quantity}, {self.price}, {self.sum}"


# Определение строки filename, которая содержит имя файла с данными о продажах
filename = 'sales_data.csv'

# Определение списка salesDB, который будет использоваться для хранения информации о продажах
salesDB = []


# Функция для загрузки информации о продажах из файла
def get_sale_info(filename):
    # Определение формата файла, исходя из его расширения
    file_format = filename.split('.')[-1]

    # Если файл в формате csv
    if file_format == 'csv':
        # Открываем файл и читаем его
        with open(filename, mode='r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовок файла
            # Для каждой строки в файле, создаем объект SaleInfo и добавляем его в список salesDB
            for row in reader:
                sale = SaleInfo(row[0], row[1], row[2], row[3], row[4], row[5])
                salesDB.append(sale)
    # Если файл в формате json
    elif file_format == 'json':
        # Читаем файл с помощью pandas
        with open(filename, 'r') as file:
            data = pd.read_json(file)
            # Для каждой строки DataFrame создаем объект SaleInfo и добавляем его в список salesDB
            for index, row in data.iterrows():
                sale = SaleInfo(row[0], row[1], row[2], row[3], row[4], row[5])
                salesDB.append(sale)
    # Если файл в формате xlsx
    elif file_format == 'xlsx':
        # Читаем файл с помощью pandas
        data = pd.read_excel(filename, engine='openpyxl')
        # Для каждой строки DataFrame создаем объект SaleInfo и добавляем его в список salesDB
        for index, row in data.iterrows():
            sale = SaleInfo(row[0], row[1], row[2], row[3], row[4], row[5])
            salesDB.append(sale)
            # Если формат файла не поддерживается
    else:
        print(f'Unsupported file format: {file_format}')
        return

    return None


# Функция для подсчета общей суммы продаж по месяцам
def total_sum_month():
    # Используем функцию getSaleInfo, чтобы загрузить данные в salesDB
    get_sale_info(filename)

    # Создаем словарь, где ключом будет год и месяц, а значением - общая сумма продаж
    month_sales = {}

    # Проходим по всем продажам в salesDB
    for sale in salesDB:
        # Представляем дату в формате год-месяц
        month_key = sale.date.strftime('%Y-%m')

        # Используем метод словаря get, который возвращает значение для данного ключа, если он существует,
        # или возвращает значение по умолчанию (0 в этом случае), если ключа не существует
        # Добавляем к предыдущей сумме для данного месяца, сумму текущей продажи
        month_sales[month_key] = month_sales.get(month_key, 0) + sale.sum

    # Выводим общую сумму продаж по месяцам
    for month, sale_sum in month_sales.items():
        print(f"Месяц: {month}, Сумма: {sale_sum:.2f}")

    # Возвращаем словарь с суммами продаж по месяцам
    return month_sales


# Функция для определения наиболее продаваемой категории товаров каждый месяц
def best_selling_category_month():
    # Загрузка информации о продажах
    get_sale_info(filename)

    # Словарь для хранения продаж по категориям для каждого месяца
    best_category_sales = {}

    # Перебор всех продаж
    for sale in salesDB:
        # Формирование ключа в формате год-месяц
        month_key = sale.date.strftime('%Y-%m')
        # Если такого месяца еще нет в словаре, добавляется новый внутренний словарь
        if month_key not in best_category_sales:
            best_category_sales[month_key] = {}
        # Добавление или увеличение количества продаж для данной категории
        best_category_sales[month_key][sale.category] = best_category_sales[month_key].get(sale.category, 0)
        best_category_sales[month_key][sale.category] += sale.quantity

    # Поиск и вывод наиболее продаваемой категории для каждого месяца
    for month, category in best_category_sales.items():
        # Поиск категории с максимальным количеством продаж
        best_category = max(category, key=category.get)
        print(f"Месяц: {month}, Лучшая категория: {best_category}")

    # Возврат словаря с продажами по категориям для каждого месяца
    return best_category_sales


# Функция для определения наиболее продаваемой категории товаров за все время
def best_selling_category_all_time():
    # Загрузим информацию о продажах
    get_sale_info(filename)
    # Создаем словарь для хранения информации о продажах по категориям
    best_category_sales = {}
    # Список для хранения дат каждой продажи
    period = []

    # Итерируем по всем продажам в salesDB
    for sale in salesDB:
        # Переводим дату каждой продажи в формат 'год-месяц-день'
        month_key = sale.date.strftime('%Y-%m-%d')
        # Добавляем данную дату в список period
        period.append(month_key)
        # Добавляем в словарь best_category_sales значения количества продаж для каждой категории или увеличиваем их,
        # если они уже есть в словаре
        best_category_sales[sale.category] = best_category_sales.get(sale.category, 0)
        best_category_sales[sale.category] += sale.quantity

    # Если список period не пустой
    if period:
        # Берем первый и последний элемент из списка period как начало и конец периода
        start_period = period[0]
        finish_period = period[-1]
    else:
        # Если данные отсутствуют, выводим сообщение об ошибке
        print("Нет данных для анализа")
        return

    # Находим категорию с наибольшим количеством продаж
    best_category = max(best_category_sales, key=best_category_sales.get)
    # Выводим сообщение с данными о лучшей категории и диапазоне дат
    print(f"Период: {start_period} - {finish_period}, Лучшая категория: {best_category}")

    # Возвращаем словарь с продажами по категориям
    return best_category_sales


# Функция для определения дня с наибольшей выручкой
def best_cost_day():
    # Загружаем информацию о продажах
    get_sale_info(filename)
    # Создаем словарь для хранения выручки по дням
    best_day_sales = {}
    # Создаем список для хранения дат каждого дня продаж
    period = []

    # Итерируемся по каждой продаже в salesDB
    for sale in salesDB:
        # Переводим дату в формат 'год:месяц:день'
        day_key = sale.date.strftime('%Y:%m:%d')
        # Добавляем дату в список периодов
        period.append(day_key)
        # Добавляем в словарь сумму текущей продажи или увеличиваем существующую сумму на эту величину
        # для каждого дня продаж
        best_day_sales[day_key] = best_day_sales.get(day_key, 0)
        best_day_sales[day_key] += sale.sum

    # Если список дат не пуст
    if period:
        # Берем первый и последний день из списка как начало и конец периода
        start_period = period[0]
        finish_period = period[-1]
    else:
        # Если данные отсутствуют, выводим сообщение об ошибке
        print("Нет данных для анализа")
        return

    # Находим день с наибольшей выручкой
    best_day = max(best_day_sales, key=best_day_sales.get)
    # Выводим период и день с наибольшей выручкой
    print(f"Период: {start_period} - {finish_period}, День с наибольшей выручкой: {best_day}")

    # Возвращаем словарь с выручкой по дням
    return best_day_sales


# Функция для определения товара с наибольшим количеством продаж за все время
def best_selling_product_all_time():
    # Загружаем информацию о продажах
    get_sale_info(filename)
    # Создаем словарь для хранения информации о продажах каждого товара
    best_product_sales = {}
    # Создаем список для хранения дат каждого дня продаж
    period = []

    # Итерируем по каждой продаже в salesDB
    for sale in salesDB:
        # Переводим дату в формат 'год:месяц:день'
        day_key = sale.date.strftime('%Y:%m:%d')
        # Добавляем дату в список period
        period.append(day_key)
        # Используем имя товара как ключ в словаре best_product_sales и добавляем сумму продажи к общей сумме продаж
        # данного товара
        product_key = sale.product
        best_product_sales[product_key] = best_product_sales.get(product_key, 0)
        best_product_sales[product_key] += sale.sum

    # Если список period не пуст
    if period:
        # Берем первый и последний день из списка как начало и конец периода
        start_period = period[0]
        finish_period = period[-1]
    else:
        # Если данные отсутствуют, выводим сообщение об ошибке
        print("Нет данных для анализа")
        return

    # Находим товар с наилучшей суммой продаж
    best_product = max(best_product_sales, key=best_product_sales.get)
    # Выводим сообщение с данными о периоде и товаре с наибольшей суммой продаж
    print(f"Период: {start_period} - {finish_period}, Лидер продаж: {best_product}")


# Функция для отображения информации о продажах по категориям в виде диаграммы
def sales_category_dashboard():
    # Вызываем функцию загрузки данных о продажах
    get_sale_info(filename)

    # Инициализируем словарь для хранения информации о продажах по категориям
    best_category_sales = {}
    # Инициализируем список для хранения всех дат продаж
    period = []

    # Итерируем по каждой категории в базе данных продаж
    for category in salesDB:
        # Считаем сумму продаж за каждую категорию и сохраняем данные в словаре
        best_category_sales[category.category] = best_category_sales.get(category.category, 0)
        best_category_sales[category.category] += category.sum
        # Преобразуем дату в строку и добавляем в список period
        day_key = category.date.strftime('%Y:%m:%d')
        period.append(day_key)

    # Проверяем, есть ли даты в списке period
    if period:
        # Если есть, то началом и концом периода будут первая и последняя даты в списке
        start_period = period[0]
        finish_period = period[-1]
    else:
        # Если дат нет, выводим сообщение об ошибке
        print("Нет данных для анализа")
        return

    # Сортируем данные о продажах по категориям в порядке убывания суммы продаж
    sorted_product_sales = sorted(best_category_sales.items(), key=lambda x: x[1], reverse=True)

    # Создаем два списка: один с названиями категорий, другой с суммами продаж
    categories = [category for category, sum in sorted_product_sales]
    sum = [sum for category, sum in sorted_product_sales]

    # Строим столбчатую диаграмму
    plt.bar(categories, sum)
    plt.xlabel('Категории', loc="center")
    plt.ylabel('Продажи')
    plt.title(f"Продажи по категориям за период {start_period} - {finish_period}")
    plt.xticks(fontsize=8, rotation=45)  # вращаем подписи категорий на 45 градусов
    plt.tight_layout()  # настраиваем автоматическую подгонку расстояний между подписями и границами графика

    # Выводим диаграмму на экран
    plt.show()

    # Возвращаем словарь с данными о продажах по категориям
    return best_category_sales


# Функция для отображения информации о выручке по дням в виде диаграммы
def sales_days_dashboard():
    # Инициализируем словарь для хранения информации о продажах по дням
    days_sales = {}
    # Вызываем функцию загрузки данных о продажах
    get_sale_info(filename)

    # Перебираем все дни продаж в базе данных
    for day in salesDB:
        # Добавляем в словарь сумму продаж за каждый день или добавляем к существующему значению
        days_sales[day.date] = days_sales.get(day.date, 0)
        days_sales[day.date] += day.sum

    # Создаем два списка: один с датами, другой с суммами продаж
    days = [day for day, sum in days_sales.items()]
    sum_sales = [sum for day, sum in days_sales.items()]

    # Устанавливаем размер графика
    plt.figure(figsize=(15, 10))
    # Преобразуем даты в числовой формат для использования в matplotlib
    days_numformat = mdates.date2num(days)
    # Строим график выручки по дням
    plt.plot_date(days_numformat, sum_sales, 'o', linestyle='-', color='b')
    plt.title('Выручка по дням')
    plt.xlabel('День')
    plt.ylabel('Выручка')
    # Форматируем ось X: делаем интервал в один день и устанавливаем формат вывода дат в виде 'год-месяц-день'
    ax = plt.gca()  # получаем текущую ось графика
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Задаем интервал в один день
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Устанавливаем формат даты
    plt.xticks(fontsize=8, rotation=90)  # вращаем подписи дат на 90 градусов
    plt.tight_layout()  # корректируем расстояние между подписями и границами графика
    plt.grid(True)  # добавляем сетку на график

    # Выводим график на экран
    plt.show()

    # Возвращаем словарь с данными о продажах по дням
    return days_sales
