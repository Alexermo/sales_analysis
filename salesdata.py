import plotly.graph_objs as go
from plotly.subplots import make_subplots
import utils


# Определение строки filepath, которая содержит имя файла с данными о продажах
filepath = 'data/sales_data.csv'
# filepath = 'data/sales_data.xlsx'
# filepath = 'data/sales_data.json'

# Функция для загрузки информации о продажах из файла
sales_data = utils.get_sales_info(filepath)


# Функция для подсчета общей суммы продаж по месяцам
def total_sum_month():
    print(utils.total_revenue_per_month(sales_data))


# Функция для определения наиболее продаваемой категории товаров каждый месяц
def best_selling_category_month():
    print(utils.most_popular_category_per_month(sales_data))


# Функция для определения наиболее продаваемой категории товаров за все время
def best_selling_category_all_time():
    print(utils.most_popular_category_overall(sales_data))


# Функция для определения дня с наибольшей выручкой
def best_cost_day():
    print(utils.day_with_highest_revenue(sales_data))


# Функция для определения товара с наибольшим количеством продаж за все время
def best_selling_product_all_time():
    print(utils.most_expensive_product(sales_data))


# Функция рисует диаграмму, график линейной зависимости продаж по дням
def print_dashboard(sales_data_df):
    # Создаем копию DataFrame, чтобы не изменять исходные данные
    df = sales_data_df.copy()

    # Создаем объект для субплотов
    fig = make_subplots(rows=2, cols=2, specs=[[{"type": "xy"}, {"type": "xy"}], [{"type": "xy"}, {"type": "domain"}]],
                        subplot_titles=('Общая стоимость продаж по категориям', 'Стоимость продаж по дням',
                                        'Доля категорий в общей стоимости продаж'))

    # Гистограмма продаж по категориям
    fig.add_trace(go.Bar(x=df['Категория продукта'], y=df['Общая стоимость продажи'], name='Стоимость'),
                  row=1, col=1)
    fig.update_xaxes(title_text='Категория', row=1, col=1)
    fig.update_yaxes(title_text='Стоимость', row=1, col=1)

    # График временного ряда стоимости продаж по дням
    fig.add_trace(go.Scatter(x=df['Дата продажи'], y=df['Общая стоимость продажи'], mode='lines', name='Стоимость'),
                  row=1, col=2)
    fig.update_xaxes(title_text='Дата', row=1, col=2)
    fig.update_yaxes(title_text='Стоимость', row=1, col=2)

    # Круговая диаграмма доли категорий в общей стоимости продаж
    category_sales = df.groupby('Категория продукта')['Общая стоимость продажи'].sum().reset_index()
    fig.add_trace(go.Pie(labels=category_sales['Категория продукта'], values=category_sales['Общая стоимость продажи'],
                         name='Стоимость'),
                  row=2, col=2)

    # Настраиваем макет дашборда
    fig.update_layout(
        height=800,
        width=1200,
        title_text='Дашборд продаж по категориям',
        title_x=0.5,
        title_font_size=24
    )

    return fig.show()


# Функция для отображения информации о продажах по категориям и по дням в виде дашборда
def sales_category_dashboard():
    print_dashboard(sales_data)
