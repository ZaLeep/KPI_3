from numpy import product
from Builder import *
from flask_restful import  reqparse
from Cache import *

class Facade:
    def __init__(self) -> None:
        self._dir = Director()
        self._parser = reqparse.RequestParser()
        self._action_product = Product()

    def create(self):
        self._parser.add_argument("CarType")
        self._parser.add_argument("Brand")
        self._parser.add_argument("Model")
        self._parser.add_argument("Price")
        self._parser.add_argument("SupplierID")
        args = self._parser.parse_args()

        self._action_product.insert(args)

    def read(self):
        return Cache().get_list()

    def update(self):
        self._parser.add_argument("CarID")
        self._parser.add_argument("CarType")
        self._parser.add_argument("Brand")
        self._parser.add_argument("Model")
        self._parser.add_argument("Price")
        self._parser.add_argument("SupplierID")
        args = self._parser.parse_args()

        self._action_product.update(args)

    def delete(self):
        self._parser.add_argument("CarID")
        args = self._parser.parse_args()
        self._action_product.delete(args["CarID"])