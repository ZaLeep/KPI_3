from pyodbc import Cursor
from ConnectSingleton import ConnectSingleton
import pandas as pd
from FilterSpecification import FilterAccumulate
import requests

class Product:
    def __init__(self) -> None:
        self.list = []
        self._conn = ConnectSingleton().conn

    def insert(self, elem):
        cursor = self._conn.cursor()
        cursor.execute("INSERT INTO Car (CarType, Brand, Model, Price, SupplierID) VALUES('%s','%s','%s','%s','%s')"%(elem["CarType"], elem["Brand"], str(elem["Model"]), str(elem["Price"]), str(elem["SupplierID"])))
        self._conn.commit()
        
    def delete(self, id):
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM Car WHERE CarID = " + str(id))
        self._conn.commit()

    def update(self, elem):
        cursor = self._conn.cursor()
        cursor.execute("UPDATE Car SET CarType = '%s', Brand = '%s', Model = '%s', Price = %s, SupplierID = %s WHERE CarID = %s"%(elem["CarType"], elem["Brand"], str(elem["Model"]), str(elem["Price"]), str(elem["SupplierID"]), str(elem["CarID"])))
        self._conn.commit()

class AbstractBuidler:
    def reset(self):
        pass
    def get_data(self, page = None):
        pass
    def processing(self):
        pass
    def filter(self):
        pass
    def get_product(self):
        pass

class BasicBuilder(AbstractBuidler):
    def __init__(self):
        self._product = None
        self._conn = ConnectSingleton().conn

    def reset(self):
        self._product = Product()

    def get_product(self):
        return self._product
    
    def get_data(self, page = None):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM Car")
        self._product.list = cursor.fetchall()

    def processing(self):
        dict_list = []
        for row in self._product.list:
            dict = {"CarID": row[0], "CarType": row[1], "Brand": row[2], "Model": row[3], "Price": row[4], "SupplierID": row[5]}
            dict_list.append(dict)
        self._product.list = dict_list

    def filter(self):
        acc = FilterAccumulate().add_all_filters()
        filter_result = []
        for dict in self._product.list:
            if acc.is_satisfied_by(dict):
                filter_result.append(dict)
        self._product.list = filter_result

class FirstServiceBuilder(AbstractBuidler):
    def __init__(self):
        self._product = None

    def reset(self):
        self._product = Product()

    def get_product(self):
        return self._product

    def get_data(self, page = None):
        self._product.list = requests.get('http://127.0.0.1:5001/search/').json()['Cars']
    
    def processing(self):
        pass

    def filter(self):
        acc = FilterAccumulate().add_all_filters()
        filter_result = []
        for dict in self._product.list:
            if acc.is_satisfied_by(dict):
                filter_result.append(dict)
        self._product.list = filter_result

class SecondServiceBuilder(AbstractBuidler):
    def __init__(self):
        self._product = None

    def reset(self):
        self._product = Product()

    def get_product(self):
        return self._product

    def get_data(self, page):
        self._product.list = requests.get('http://127.0.0.1:5002/price-list/' + str(page)).json()['Cars']
    
    def processing(self):
        final_list = []
        for d in self._product.list:
            new_dict = dict(d)
            add = requests.get('http://127.0.0.1:5002/details/' + str(d['CarID'])).json()
            new_dict.update(add)
            final_list.append(new_dict)
        self._product.list = final_list

    def filter(self):
        acc = FilterAccumulate().add_all_filters()
        filter_result = []
        for dict in self._product.list:
            if acc.is_satisfied_by(dict):
                filter_result.append(dict)
        self._product.list = filter_result

class Director:
    def __init__(self):
        self._buider = None

    def set_builder(self, builder):
        self._buider = builder

    def get_builder(self):
        return self._buider

    def build_whole_list(self, page = None):
        self._buider.reset()
        self._buider.get_data(page)
        self._buider.processing()

    def build_filter_list(self, page = None):
        self._buider.reset()
        self._buider.get_data(page)
        self._buider.processing()
        self._buider.filter()

    def get_result(self):
        return self._buider.get_product().list