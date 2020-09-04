from random import randint, choice
from monopolyProperties import *

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500 #Starting money $1500
        self.position = 0 #Board position
        self.ownedProperties = [] #array of their owned properties, unsure what this is for
        self.jailed = 0 #How many turns player has left in jail
        self.jailfree = 0 #Get out of jail free cards
        self.houses = 0
        self.hotels = 0
        self.doubles = 0 #How many doubles in a row they have

playerlist = []

def jail(player):
    if player.jailfree == 0:
        player.jailed = 3
    else:
        player.jailfree -= 1
    player.position = 10

def payJail(player):
    if player.money < 50:
        print("You don't have enough money to pay to get out of Jail!")
        return False
    else:
        print("You paid $50 to get out of jail.")
        player.money -= 50
        return True

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

        if propertylist[player.position].owner == None: #buy or pay
            propertylist[player.position].buy(player)
        else:
            propertylist[player.position].rent(player, 50)

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
    print("Rolling dice...")
    global dice1, dice2, diceSum
    dice1, dice2 = randint(1,6), randint(1,6)
    print(f"You rolled a {dice1} and a {dice2}!")
    diceSum = dice1+dice2

def movePlayer(player, diceSum):
    print(f"You move {diceSum} spaces.")
    player.position += diceSum
    if player.position >= 39:
        player.position -= 39
        player.money += 200
    print(f"You land on {propertylist[player.position].name}.")
    propertylist[player.position].land(player)

def startGame():
    print("Welcome to scuffed Monopoly!")
    global playercount, playing
    playercount = int(input("How many people are playing? (2-4)"))
    for i in range(int(playercount)):
        name = input(f"Player {i+1}'s name? > ")
        name = Player(name)
        playerlist.append(name)
    playing = True

def turnOptions(player):
    print("What would you like to do?")
    print("Options: Roll (r), View Assets (v)")
    while True:
        response = input("> ")
        if response in ["r", "v"]:
            if response == "r":
                break
            elif response == "v":
                print(f"Current balance: ${player.money}")
                print("Owned properties: ", end=" ")
                for property in player.ownedProperties:
                    print(f"{property.name}", end=", ")
                print("\n")
                turnOptions(player)
                break
        else:
            print("Invalid input!")

def jailedOptions(player):
    print("What would you like to do?")
    print("Options: Roll (r), View Assets (v), Pay $50 to get out of Jail (p)")
    while True:
        response = input("r/v/p? > ")
        if response in ["r", "v", "p"]:
            if response == "r":
                rollDice()
                if dice1 == dice2:
                    print("You rolled doubles, you get out of jail!")
                    player.jailed = 0
                    movePlayer(player, diceSum)
                else:
                    print("You didn't roll doubles.")
                    if player.jailed == 1:
                        print("Since you didn't roll doubles on your 3rd turn",
                        "in jail, you have to pay $50 to get out.")
                        if payJail(player):
                            moveplayer(player, diceSum)
                    else:
                        print("You remain in jail.")
            elif response == "v":
                print(f"Current balance: {player.money}")
                print("Owned properties: ", end=" ")
                for property in player.ownedProperties:
                    print(f"{property.name}", end=", ")
                jailedOptions(player)
            elif response == "p":
                if payJail(player):
                    rollDice()
                    movePlayer()
                else:
                    print("You remain in jail.")


def endGame(player):
    global playing
    print(f"{player.name} went bankrupt!")
    playing = False

startGame()
while playing:
    for i in range(playercount):
        player = playerlist[i]
        print(f"\n{player.name}'s turn.\n")

        if player.jailed == 0:
            turnOptions(player)
            rollDice()
            movePlayer(player, diceSum)
        else:
            jailedOptions()

        if playing == False:
            break
