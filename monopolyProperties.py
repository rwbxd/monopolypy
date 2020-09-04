import csv
import random

class boardSpace:
    def __init__(self, name, category):
        self.name = name
        self.category = category

class Corner(boardSpace):
    def __init__(self,name,category):
        super().__init__(name, category)

    def land(self, player):
        pass

class Property(boardSpace):
    def __init__(self, name, category, price, rent):
        super().__init__(name, category)
        self.price = int(price)
        self.rent = int(rent)
        self.owner = None

    def land(self, player):
        if self.owner == None:
            self.buy(player)
        elif self.owner != player:
            self.rent(player)
        else:
            pass

    def rent(self, player):
        if player.money < self.rent:
            print(f"{player.name} doesn't have enough money to pay rent to {self.owner.name}!")
        else:
            print(f"{player.name} pays ${self.rent} to {self.owner.name}!")
            player.money -= rent
            self.owner.money += rent

    def buy(self, player):
        if player.money < self.price:
            print("You don't have enough money to buy this property!")
        else:
            print(f"Do you want to buy {self.name}?")
            print(f"It costs {self.price}, and you have {player.money}.")
            while True:
                response = input("y/n? > ")
                if response in ["Y", "y", "yes", "Yes", "n", "N", "no", "No"]:
                    break
                else:
                    print("Invalid input!")
            if response in ["Y", "y", "yes", "Yes"]:
                self.owner = player
                player.money -= self.price
                player.ownedProperties.append(self)

class Utility(boardSpace):
    def __init__(self, name, category, price):
        super().__init__(name, category)
        self.price = int(price)
        self.owner = None

    def land(self,player):
        if self.owner == None:
            self.buy(player)
        elif self.owner != player:
            self.rent(player)
        else:
            pass

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

    def buy(self, player):
        if player.money < self.price:
            print("You don't have enough money to buy this property!")
        else:
            print(f"Do you want to buy {self.name}?")
            print(f"It costs {self.price}, and you have {player.money}.")
            while True:
                response = input("y/n? > ")
                if response in ["Y", "y", "yes", "Yes", "n", "N", "no", "No"]:
                    break
                else:
                    print("Invalid input!")
            if response in ["Y", "y", "yes", "Yes"]:
                self.owner = player
                player.money -= self.price
                player.ownedProperties.append(self)

class Railroad(boardSpace):
    def __init__(self, name, category, price):
        super().__init__(name, category)
        self.price = int(price)
        self.owner = None

    def land(self,player):
        if self.owner == None:
            self.buy(player)
        elif self.owner != player:
            self.rent(player, 25)
        else:
            pass

    def rent(self, player, amount): #I do this for the chance card that doubles rent payout
        check = 5
        owned = 0
        while check < 35:
            if propertylist[check].owner == self.owner:
                owned += 1
            check += 10
        pay = amount * owned
        print(f"{player} pays {self.owner} ${pay} in rent!")
        player.money -= pay
        self.owner += pay

    def buy(self, player):
        if player.money < self.price:
            print("You don't have enough money to buy this property!")
        else:
            print(f"Do you want to buy {self.name}?")
            print(f"It costs {self.price}, and you have {player.money}.")
            while True:
                response = input("y/n? > ")
                if response in ["Y", "y", "yes", "Yes", "n", "N", "no", "No"]:
                    break
                else:
                    print("Invalid input!")
            if response in ["Y", "y", "yes", "Yes"]:
                self.owner = player
                player.money -= self.price
                player.ownedProperties.append(self)

class CC(boardSpace):
    def __init__(self, name, category):
        super().__init__(name, category)

    def land(self, player):
        with open("communityChest.csv", "r") as f:
            reader = csv.reader(f)
            row = random.choice(list(reader))
            print(f"The card reads: {row[0]}")
            exec(row[1])

class Tax(boardSpace):
    def __init__(self, name, category, taxprice):
        super().__init__(name, category)
        self.taxprice = int(taxprice)

    def land(self, player):
        print(f"{player} pays ${taxprice}.")
        player.money -= taxprice

class Chance(boardSpace):
    def __init__(self, name, category):
        super().__init__(name, category)

    def land(self, player):
        with open("chance.csv", "r") as f:
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

def initProperties():
    with open("monopolyProperties.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader: #boardSpace with row[0] row[1], add to boardlist, for i in boardlist,
            if row[1] in ["CC", "tax", "chance", "corner", "gotojail", "utility", "railroad"]:
                #propertylist.append(exec(row[1](row[0],row[1])))
                #Above snippet doesn't work AFAIK, but it'd eliminate a lot of code
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
                elif row[1] == "railroad":
                    propertylist.append(Railroad(row[0],row[1],row[2]))
            else:
                propertylist.append(Property(row[0],row[1],row[2],row[3]))

initProperties()
