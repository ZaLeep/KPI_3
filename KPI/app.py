from ConnectSingleton import ConnectSingleton
from flask import Flask, request
from flask_restful import Api
from QueryChain import *
from Cache import Cache
import time

if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    Cache().init_cache()
    @app.route("/get_cars/", methods=['POST', 'GET', 'PUT', 'DELETE'])
    def run():
        start = time.time()
        create = CreateHandler()
        read = ReadHandler()
        update = UpdateHandler()
        delete = DeleteHandler()
        create.set_next_handler(read.set_next_handler(update.set_next_handler(delete)))
        res = create.handle(request.method)
        print("========================================================================")
        print(time.time() - start)
        print("========================================================================")
        return res
    app.run(debug=True)
    ConnectSingleton().conn.close()
