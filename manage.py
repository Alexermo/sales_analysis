import time

from salesdata import (best_cost_day, best_selling_category_all_time,
                       best_selling_category_month,
                       best_selling_product_all_time, sales_category_dashboard, total_sum_month)


def start():
    """
    Запускает главный цикл программы, в котором предлагает пользователю выбор одну из 7 опций.
    Если происходит ошибка, она отлавливается и выводится на экран.
    """
    try:
        # Главный цикл программы
        while True:
            print()
            print("ВЫБЕРЕТЕ ОДНУ ИЗ ОПЦИЙ:")
            print()
            print("1. Показать выручку по месяцам")
            print("2. Показать самую продаваемую категорию в каждом месяце")
            print("3. Показать самую продаваемую категорию за все время")
            print("4. Показать продукт - Лидер продаж за все время")
            print("5. Показать день с наибольшей выручкой за все время")
            print("6. Показать график продаж по категориям")
            print("8. Выйти")
            print()

            option = input("ВАШ ВЫБОР: ")

            match option:
                case '1':
                    total_sum_month()
                    time.sleep(3)
                case '2':
                    best_selling_category_month()
                    time.sleep(3)
                case '3':
                    best_selling_category_all_time()
                    time.sleep(3)
                case '4':
                    best_selling_product_all_time()
                    time.sleep(3)
                case '5':
                    best_cost_day()
                    time.sleep(3)
                case '6':
                    sales_category_dashboard()
                    time.sleep(3)
                case '8':
                    break
                case _:
                    print("Введен неверный параметр, попробуйте еще раз.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    start()
