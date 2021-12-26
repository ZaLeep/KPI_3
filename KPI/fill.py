import random as rd
from ConnectSingleton import *
from string import ascii_letters


def fill_base():
    conn = ConnectSingleton().conn
    cursor = conn.cursor()
    for i in range(100000):
        CarType = rd.choice(["Hatchback", "Univerasl", "Sedan", "Pickup", "Wagon", "Compact", "Coupe"])
        Brand = rd.choice(["BMW", "Mercedes Benz", "Lada", "Renault", "Audi", "Subaru", "Tesla", "Opel"])
        Model = "".join(rd.choice(ascii_letters) for i in range(7))
        Price = rd.randint(500, 3000)
        Supplier = rd.randint(1, 5)
        cursor.execute("INSERT INTO Car(CarType, Brand, Model, Price, SupplierID) VALUES('" + CarType + "', '" + Brand + "', '" + Model + "', " + str(Price) + ", " + str(Supplier) + ")")
        cursor.commit()

def fill_second():
    conn = Connect2Singleton().conn
    cursor = conn.cursor()
    for i in range(50000):
        CarType = rd.choice(["Hatchback", "Univerasl", "Sedan", "Pickup", "Wagon", "Compact", "Coupe"])
        Brand = rd.choice(["BMW", "Mercedes Benz", "Lada", "Renault", "Audi", "Subaru", "Tesla", "Opel"])
        Model = "".join(rd.choice(ascii_letters) for i in range(7))
        Price = rd.randint(500, 3000)
        Supplier = rd.randint(1, 5)
        cursor.execute("INSERT INTO CarPrice(CarID, Brand, Model, Price) VALUES (" + str(i) + ", '" + Brand + "', '" + Model + "', " + str(Price) + ")")
        cursor.execute("INSERT INTO CarDetails(CarID, CarType, Supplier) VALUES (" + str(i) + ", '" + CarType + "', " + str(Supplier) + ")")
        cursor.commit()

fill_second()