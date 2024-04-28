import os
import sqlalchemy
import psycopg2
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, drop_tables, Publisher, Book, Shop, Stock, Sale

BASE_PATH = os.getcwd()
DATA_DIR = 'fixtures'
DATA = 'tests_data.json'

sql_db = 'postgresql'
login = 'postgres'
password = 'Ingrad2022'
name_db = 'sale-book'

with open(os.path.join(BASE_PATH, DATA_DIR, DATA), 'r') as f:
    file_content = f.read()
    data = json.loads(file_content)

# DSN = 'используемая БД :// логин ДБ : пароль ДБ @ имя сервера : порт сервера (5432) / название ДБ'
DSN = f'{sql_db}://{login}:{password}@localhost:5432/{name_db}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)

# извлечение данных из tests_data помещение моделей в список
def update_db(data):
    add_list = []
    for element in data:
        if element['model'] == 'publisher':
            name = element['fields']['name']
            publisher = Publisher(name=name)
            add_list.append(publisher)
        elif element['model'] == 'book':
            title = element['fields']['title']
            id_publisher = element['fields']['id_publisher']
            book = Book(title=title, id_publisher=id_publisher)
            add_list.append(book)
        elif element['model'] == 'shop':
            name = element['fields']['name']
            shop = Shop(name=name)
            add_list.append(shop)
        elif element['model'] == 'stock':
            id_shop = element['fields']['id_shop']
            id_book = element['fields']['id_book']
            count = element['fields']['count']
            stock = Stock(id_shop=id_shop, id_book=id_book, count=count)
            add_list.append(stock)
        elif element['model'] == 'sale':
            price = element['fields']['price']
            date_sale = element['fields']['date_sale']
            count = element['fields']['count']
            id_stock = element['fields']['id_stock']
            sale = Sale(price=price, date_sale=date_sale, count=count, id_stock=id_stock)
            add_list.append(sale)
    session.add_all(add_list)
    session.commit()

# найти по имени или id издателя вывести магазины где он продается
def find_shop():
    tmp = input("Введите имя или номер издателя: ")
    if tmp.isdigit() == True:
        for c in session.query(Publisher, Shop).join(Book).join(Stock).join(Shop).filter(Publisher.id == f'{tmp}').all():
            print(*c, sep=' | ')
    else:
        for c in session.query(Publisher, Shop).join(Book).join(Stock).join(Shop).filter(Publisher.name.ilike(f'%{tmp}%')).all():
            print(*c, sep=' | ')


if __name__ == "__main__":
    # create_tables(engine)
    # drop_tables(engine)
    session = Session()
    # update_db(data)
    find_shop()
    session.close()
