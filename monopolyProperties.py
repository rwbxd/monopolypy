import csv
import random

class boardSpace:
    def __init__(self, name, category):
        self.name = name
        self.category = category

class Corner(boardSpace):
    def __init__(self,name,category):
        super().__init__(name, category)

class Property(boardSpace):
    def __init__(self, name, category, price, rent):
        super().__init__(name, category)
        self.price = int(price)
        self.rent = int(rent)
        self.owner = None

        def rent(player):
            pass

class Utility(boardSpace):
    def __init__(self, name, category, price):
        super().__init__(name, category)
        self.price = price
        self.owner = None

    def rent(self, player):
        if propertylist[12].owner == propertylist[28].owner:
            pay = 10 * diceSum
        else:
            pay = 4 * diceSum
        player.money -= pay
        self.owner += pay
        print(f"{player} pays {self.owner} ${pay} in rent!")

    def rentForced(self, player):
        pay = 10 * diceSum
        player.money -= pay
        self.owner += pay
        print(f"{player} pays {self.owner} ${pay} in rent!")

class CC(boardSpace):
    def __init__(self, name, category):
        super().__init__(name, category)

    def land(self, player):
        with open("C:/Users/Will/Desktop/Python/monopoly/communityChest.csv", "r") as f:
            reader = csv.reader(f)
            row = random.choice(list(reader))
            print(f"The card reads: {row[0]}")
            exec(row[1])

class Tax(boardSpace):
    def __init__(self, name, category, taxprice):
        super().__init__(name, category)
        self.taxprice = int(taxprice)

    def land(self, player):
        print(f"{player} pays ${taxprice}.)
        player.money -= taxprice

class Chance(boardSpace):
    def __init__(self, name, category):
        super().__init__(name, category)

    def land(self, player):
        with open("C:/Users/Will/Desktop/Python/monopoly/chance.csv", "r") as f:
            reader = csv.reader(f)
            row = random.choice(list(reader))
            print(f"The card reads {row[0]}")
            exec(row[1])

class Gotojail(boardSpace):
    def __init__(self, name, category):
        super().__init__(name, category)

    def land(self, player):
        print(f"{player} is sent to jail! {player} doesn't pass go, nor do they collect $200!")
        jail(player)


propertylist = []

with open("C:/Users/Will/Desktop/Python/monopoly/monopolyProperties.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader: #boardSpace with row[0] row[1], add to boardlist, for i in boardlist,
        if row[1] in ["CC", "tax", "chance", "corner", "gotojail"]:
            if row[1] == "CC":
                propertylist.append(CC(row[0],row[1]))
            elif row[1] == "tax":
                propertylist.append(Tax(row[0],row[1],row[3]))
            elif row[1] == "chance":
                propertylist.append(Chance(row[0],row[1]))
            elif row[1] == "corner":
                propertylist.append(Corner(row[0],row[1]))
            elif row[1] == "gotojail":
                propertylist.append(Gotojail(row[0],row[1]))
            elif row[1] == "utility":
                propertylist.append(Utility(row[0],row[1],row[2]))
        else:
            propertylist.append(Property(row[0],row[1],row[2],row[3]))
