from flask import Flask
from flask_restful import Api
from ConnectSingleton import Connect2Singleton

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    @app.route('/price-list/<int:page>', methods = ['GET'])
    def run_prices(page):
        car_price = []
        conn = Connect2Singleton().conn
        cursor = conn.cursor()
        cursor.execute("SELECT TOP(5000) * FROM CarPrice WHERE CarID NOT IN(SELECT TOP(5000 * " + str(page - 1) + ") CarID FROM CarPrice)")
        for row in cursor.fetchall():
            car_price.append({'Page': page, 'CarID': row[0], 'Brand': row[1], 'Model': row[2], 'Price': float(row[3])})
        return {"Cars": car_price}

    @app.route('/details/<int:car_id>', methods = ['GET'])
    def run_details(car_id):
        conn = Connect2Singleton().conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CarDetails WHERE CarID = " + str(car_id))
        row = cursor.fetchone()
        res = {'CarID': row[0], 'CarType': row[1], 'SupplierID': row[2]}
        return res

    app.run(port = 5002, debug = False)