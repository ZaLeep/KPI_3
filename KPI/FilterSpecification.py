from abc import abstractmethod
from flask_restful import  reqparse

class Specification:
    def is_satisfied_by(self, elem):
        pass

class CarType(Specification):
    def is_satisfied_by(self, elem):
        parser = reqparse.RequestParser().add_argument("CarType")
        args = parser.parse_args()
        if args['CarType']:
            return elem['CarType'] == args['CarType']
        else:
            return True

class CarModel(Specification):
    def is_satisfied_by(self, elem):
        parser = reqparse.RequestParser().add_argument("Model")
        args = parser.parse_args()
        if args['Model']:
            return elem['Model'] == args['Model']
        else:
            return True

class MinPrice(Specification):
  def is_satisfied_by(self, elem):
      parser = reqparse.RequestParser().add_argument("min_price")
      args = parser.parse_args()
      if args['min_price']:
          return float(elem['Price']) > float(args['min_price'])
      else:
          return True

class MaxPrice(Specification):
  def is_satisfied_by(self, elem):
      parser = reqparse.RequestParser().add_argument("max_price")
      args = parser.parse_args()
      if args['max_price']:
          return float(elem['Price']) < float(args['max_price'])
      else:
          return True


class FilterAccumulate:
    def __init__(self):
        self._filters = []

    def is_satisfied_by(self, elem):
        return all([filters.is_satisfied_by(elem) for filters in self._filters])
    
    def add_all_filters(self):
        self.add_type_filter()
        self.add_model_filter()
        self.add_price_filter()
        return self

    def add_type_filter(self):
        self._filters.append(CarType())
    def add_model_filter(self):
        self._filters.append(CarModel())
    def add_price_filter(self):
        self._filters.append(MinPrice())
        self._filters.append(MaxPrice())