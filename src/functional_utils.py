from functools import reduce

##### FILTER #####

def is_category(category):
    def inner(sale):
        return sale.category == category
    return inner

def filter_sales_by_category(sales, category):
    return list(filter(is_category(category), sales))

def is_client(client_id):
    def inner(sale):
        return sale.client_id == client_id
    return inner

def filter_sales_by_client(sales, client_id):
    return list(filter(is_client(client_id), sales))

def is_date(date):
    def inner(sale):
        return sale.date == date
    return inner

def filter_sales_by_date(sales, date):
    return list(filter(is_date(date), sales))

def is_month(month):
    def inner(sale):
        return sale.date.startswith(month)
    return inner

def filter_sales_by_month(sales, month):
    return list(filter(is_month(month), sales))



##### MAP #####

def sale_to_amount(sale):
    return sale.amount

def map_sales_to_amount(sales):
    return list(map(sale_to_amount, sales))

def sale_to_category(sale):
    return sale.category

def map_sales_to_category(sales):
    return list(map(sale_to_category, sales))

def sale_to_dict(sale):
    return {
        "sale_id": sale.sale_id,
        "client_id": sale.client_id,
        "product": sale.product,
        "category": sale.category,
        "amount": sale.amount,
        "date": sale.date
    }

def map_sales_to_dict(sales):
    return list(map(sale_to_dict, sales))



##### REDUCE #####

def sum_amount(acc, sale):
    return acc + sale.amount

def total_amount(sales):
    return reduce(sum_amount, sales, 0)

def average_amount(sales):
    if len(sales) == 0:
        return 0
    return total_amount(sales) / len(sales)



##### GROUP #####

def group_by_category(sales):
    result = {}

    for sale in sales:
        category = sale.category
        result.setdefault(category, []).append(sale)

    return result

def group_by_month(sales):
    result = {}

    for sale in sales:
        month = sale.date[:7]
        result.setdefault(month, []).append(sale)

    return result

def summary_by_category(sales):
    grouped = group_by_category(sales)

    result = {}

    for category, sales_list in grouped.items():
        result[category] = total_amount(sales_list)

    return result