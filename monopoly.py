from random import randint, choice
from monopolyProperties import *
from extraSpaces import *

diceSum, dice1, dice2 = 0,0,0 #Using global variables to make my life easier
#May change to pass into functions again

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500 #Starting money $1500
        self.position = 0 #Board position
        self.ownedProperties = [] #array of their owned properties, unsure what this is for
        self.jailed = False #
        self.jailfree = 0 #Get out of jail free cards
        self.houses = 0
        self.hotels = 0

playerlist = []

def jail(player):
    if player.jailfree = 0:
        player.jailed = True
    else:
        player.jailfree -= 1
    player.position = 9

def collectfromall(player, amount):
    for i in range(playercount):
        playerlist[i].money -= amount
    player.money += (amount * playercount)

def advanceto(player, where):
    if where == "railroad": #5, 15, 25, 35
        if player.position > 35:
            player.money += 200
            player.position = 5
        else:
            if player.position > 25: #Impossible for them to be on a railroad
                player.position = 35
            elif player.position > 15:
                player.position = 25
            elif player.position > 5:
                player.position = 15
            else:
                player.position = 5
    elif where == "utility": #12, 28
        if player.position > 28: #move player
            player.money += 200
            player.position = 12
        elif player.position <= 12:
            player.position = 12
        else:
            player.position = 28

        if propertylist[player.position].owner == None: #buy or pay
            propertylist[player.position].buy(player)
        else:
            rollDice()
            propertylist[player.position].rentForced(player)

def rollDice():
    global dice1, dice2, diceSum
    dice1, dice2 = randint(1,6), randint(1,6)
    print(f"You rolled a {dice1} and a {dice2}!")
    diceSum = dice1+dice2

def determinePosition(player, diceSum):
    player.position += diceSum
    if player.position >= 39:
        player.position -= 39
        player.money += 200
    print(f"{player} lands on {propertylist[player.position].name}.)

def determineType(player):
    currentProperty = propertylist[player.position]
    if currentProperty.category in ["CC", "tax", "chance", "corner", "gotojail"]:
        #do custom stuff
        pass
    else:
        determineOwner(player)

def determineOwner(player):
    currentProperty = propertylist[player.position]
    if currentProperty.owner == player:
        pass
    elif currentProperty.owner == None:
        buyProperty(currentProperty, player)
    else:
        payRent(currentProperty, player)

def buyProperty(property, player):
    if player.money < property.price:
        print("You don't have enough money to buy this property!")
    else:
        print(f"Do you want to buy {property.name}?")
        print(f"It costs {property.price}, and you have {player.money}.\n")
        response = input()
        if response in ["Y", "y"]:
            property.owner = player
            player.money -= property.price
            player.ownedProperties.append(property)

def payRent(property, player):
    owner = property.owner
    rent = property.rent
    if player.money < property.rent:
        print(f"{player.name} doesn't have enough money to pay rent to {owner.name}!")
    else:
        print(f"{player.name} pays ${rent} to {owner.name}!")
        player.money -= rent
        owner.money += rent

def startGame():
    print("Welcome to scuffed Monopoly!")
    global playercount
    playercount = int(input("How many people are playing? (2-4)"))
    for i in range(int(playercount)):
        name = input(f"Player {i+1}'s name? > ")
        name = Player(name)
        playerlist.append(name)

startGame()
while not any(x.money <= 0 for x in playerlist):
    print(*playerlist)
    for i in range(playercount):
        rollDice(playerlist[i])
    playerlist[0].money = 0
