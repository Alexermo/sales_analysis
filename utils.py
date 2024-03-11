import pandas as pd


def total_revenue_per_month(sales_data):
    """
    Подсчет общей выручки по каждому месяцу
    """
    # Группировка по месяцу и подсчет общей выручки
    monthly_revenue = sales_data.groupby(sales_data['Дата продажи'].dt.to_period('M'))['Общая стоимость продажи'].sum()\
        .reset_index()
    return monthly_revenue


def most_popular_category_per_month(sales_data):
    """
    Нахождение самой популярной категории продуктов в каждом месяце
    """
    # Группировка по месяцу и категории, подсчет количества проданных единиц
    monthly_category_sales = sales_data.groupby([sales_data['Дата продажи'].dt.to_period('M'), 'Категория продукта'])[
        'Количество проданных единиц'].sum()
    # Нахождение самой популярной категории в каждом месяце
    most_popular_categories = monthly_category_sales.groupby(level=0).idxmax().str[1]
    most_popular_categories = most_popular_categories.reset_index()
    most_popular_categories.rename(columns={'Количество проданных единиц': 'Категория продукта'}, inplace=True)
    return most_popular_categories


def most_popular_category_overall(sales_data):
    """
    Нахождение самой популярной категории продуктов за всё время
    """
    # Подсчет количества проданных единиц по категории
    category_sales = sales_data.groupby('Категория продукта')['Количество проданных единиц'].sum()
    # Нахождение самой популярной категории
    most_popular_category = category_sales.idxmax()
    return most_popular_category


def most_expensive_product(sales_data):
    """
    Нахождение продукта с самой высокой общей стоимостью продаж
    """
    # Группировка по продукту и подсчет общей стоимости продаж
    product_sales = sales_data.groupby('Продукт')['Общая стоимость продажи'].sum()
    # Нахождение продукта с самой высокой общей стоимостью продаж
    expensive_product = product_sales.idxmax()
    return expensive_product


def day_with_highest_revenue(sales_data):
    """
    Нахождение дня с наибольшей выручкой
    """
    # Группировка по дате и подсчет общей выручки
    daily_revenue = sales_data.groupby(sales_data['Дата продажи'].dt.date)['Общая стоимость продажи'].sum()
    # Нахождение дня с наибольшей выручкой
    highest_revenue_day = daily_revenue.idxmax()
    return highest_revenue_day


def read_csv_file(filepath):
    data = pd.read_csv(
        filepath,
        sep=',',
        header=None,
        skiprows=1,
        names=['Дата продажи', 'Продукт', 'Категория продукта',
               'Количество проданных единиц', 'Цена за единицу', 'Общая стоимость продажи'],
        dtype={'Дата продажи': object, 'Продукт': str, 'Категория продукта': str,
               'Количество проданных единиц': int, 'Цена за единицу': float, 'Общая стоимость продажи': float}
    )
    # Convert 'Дата продажи' к типу date
    data['Дата продажи'] = pd.to_datetime(data['Дата продажи'])
    return data


def read_xlsx_file(file_path, sheet_name=None):
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    if isinstance(data, dict):
        # Если возвращается словарь, выбираем первый DataFrame
        data = next(iter(data.values()))
    # Convert 'Дата продажи' к типу date
    data['Дата продажи'] = pd.to_datetime(data['Дата продажи'])
    return data


def read_json_file(file_path, orient='columns'):
    data = pd.read_json(file_path, orient=orient)
    # Convert 'Дата продажи' к типу date
    data['Дата продажи'] = pd.to_datetime(data['Дата продажи'])
    return data


def get_sales_info(sales_data_file_path):
    file_extension = sales_data_file_path.split('.')[-1]

    match file_extension:
        case 'csv':
            data = read_csv_file(sales_data_file_path)
        case 'xlsx':
            data = read_xlsx_file(sales_data_file_path)
        case 'json':
            data = read_json_file(sales_data_file_path)
        case _:
            print("Unsupported file format.")
            return

    return data
