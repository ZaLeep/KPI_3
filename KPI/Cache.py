from Builder import *
from flask_restful import  reqparse
from FilterSpecification import *

class Cache():

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Cache, cls).__new__(cls)
        return cls.instance
    
    def init_cache(self):  
        self._base_cache = []
        self._first_cache = []
        self._second_cache = []
        self.init_base()
        print(self._base_cache[0])
        print(self._base_cache[len(self._base_cache) - 1])
        self.init_first()
        print(self._first_cache[0])
        print(self._first_cache[len(self._first_cache) - 1])
        self.init_second()
        print(self._second_cache[0])
        print(self._second_cache[len(self._second_cache) - 1])

    def init_base(self):
        director = Director()
        director.set_builder(BasicBuilder())
        director.build_whole_list()
        self._base_cache = director.get_result()

    def init_first(self):
        director = Director()
        director.set_builder(FirstServiceBuilder())
        director.build_whole_list()
        self._first_cache = director.get_result()

    def init_second(self):
        director = Director()
        director.set_builder(SecondServiceBuilder())
        page = 1
        last_res = [0]
        while(len(last_res) != 0):
            director.build_whole_list(page)
            some_result = director.get_result()
            page += 1
            if len(some_result) != 0:
                self._second_cache += some_result
            last_res = some_result

    def get_list(self):
        parser = reqparse.RequestParser()
        parser.add_argument("CarType")
        parser.add_argument("Model")
        parser.add_argument("min_price")
        parser.add_argument("max_price")
        args = parser.parse_args()
        acc = FilterAccumulate()
        if args['CarType']:
            acc.add_type_filter()
        if args['Model']:
            acc.add_model_filter()
        if args['min_price'] or args['max_price']:
            acc.add_price_filter()
        result = []
        for dict in self._base_cache:
            if acc.is_satisfied_by(dict):
                result.append(dict)
        for dict in self._first_cache:
            if acc.is_satisfied_by(dict):
                result.append(dict)
        for dict in self._second_cache:
            if acc.is_satisfied_by(dict):
                result.append(dict)
        return result
        
    def filter(self, result, list, acc):
        for dict in list:
            if acc.is_satisfied_by(dict):
                result.append(dict)