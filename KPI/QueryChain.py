from Facade import Facade

class Handler():
    def set_next_handler(self, handler):
        pass

    def handle(self, request):
        pass

class AbstractHandler(Handler):
    _next_handler: Handler = None
    _facade: Facade = Facade()

    def set_next_handler(self, handler):
        self._next_handler = handler
        return self

    def handle(self, request):
        pass

class CreateHandler(AbstractHandler):
    def handle(self, request):
        if request == 'POST':
            self._facade.create()
            return "Created."
        elif self._next_handler != None:
            return self._next_handler.handle(request)
        return "Unknown request1."

class ReadHandler(AbstractHandler):
    def handle(self, request):
        if request == 'GET':
            return {"Cars": self._facade.read()}
        elif self._next_handler != None:
            return self._next_handler.handle(request)
        return "Unknown request2."
    
class UpdateHandler(AbstractHandler):
    def handle(self, request):
        if request == 'PUT':
            self._facade.update()
            return "Updated."
        elif self._next_handler != None:
            return self._next_handler.handle(request)
        return "Unknown request3."

class DeleteHandler(AbstractHandler):
    def handle(self, request):
        if request == 'DELETE':
            self._facade.delete()
            return "Deleted."
        elif self._next_handler != None:
            return self._next_handler.handle(request)
        return "Unknown request4."