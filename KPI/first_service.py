from flask import Flask
from flask_restful import Api
import time

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    @app.route('/search/', methods = ['GET'])
    def run():
        cars = [{'CarID': 11, 'CarType': 'Universal', 'Brand': 'Mercedes-Benz', 'Model': 'GL550', 'Price': 3250.0, 'SupplierID': 1},
                {'CarID': 12, 'CarType': 'Sedan', 'Brand': 'Toyota', 'Model': 'Corolla 2019', 'Price': 1500.0, 'SupplierID': 3}]
        #time.sleep(30)
        return {"Cars": cars}
    app.run(port = 5001, debug = True)