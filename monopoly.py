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

def payJail(player):
    if player.money < 50:
        print("You don't have enough money to pay to get out of Jail!")
        return False
    else:
        print("You paid $50 to get out of jail.")
        player.money -= 50
        return True

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
    while True:
        playercount = input("How many people are playing? (2-6)\n> ")
        try:
            playercount = int(playercount)
        except:
            print("Invalid input! Please enter a number between 2 and 6!")
        else:
            if (playercount > 1 and playercount <= 6):
                break
            else:
                print("Invalid number! Please enter a number between 2 and 6!")
    for i in range(playercount):
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
                    break
                else:
                    print("You didn't roll doubles.")
                    if player.jailed == 1:
                        print("Since you didn't roll doubles on your 3rd turn",
                        "in jail, you have to pay $50 to get out.")
                        if payJail(player):
                            player.jailed = 0
                            movePlayer(player, diceSum)
                            break
                    else:
                        player.jailed -= 1
                        print("You remain in jail.")
                        break
            elif response == "v":
                print(f"Current balance: {player.money}")
                print("Owned properties: ", end=" ")
                for property in player.ownedProperties:
                    print(f"{property.name}", end=", ")
                jailedOptions(player)
            elif response == "p":
                if payJail(player):
                    player.jailed = 0
                    rollDice()
                    movePlayer(player, diceSum)
                    break
                else:
                    print("You remain in jail.")


def endGame(player):
    global playing
    print(f"{player.name} went bankrupt!")
    playing = False
    input()

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
            jailedOptions(player)

        if playing == False:
            break
