import pyodbc as db

class ConnectSingleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConnectSingleton, cls).__new__(cls)
        return cls.instance
    def __init__(self) -> None:
        self.conn = db.connect("Driver={SQL Server};Server=DESKTOP-3UDI7MO;Database=CarRent;Trusted_Connection=yes;")

class Connect2Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connect2Singleton, cls).__new__(cls)
        return cls.instance
    def __init__(self) -> None:
        self.conn = db.connect("Driver={SQL Server};Server=DESKTOP-3UDI7MO;Database=CarRent2;Trusted_Connection=yes;")