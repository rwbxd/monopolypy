from random import randint
from monopolyProperties import *

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500 #Starting money $1500
        self.position = 0 #Board position, start on GO
        self.ownedProperties = [] #array of their owned properties
        self.propertyGroups = [] #full color sets
        self.jailed = 0 #How many turns player has left in jail
        self.jailfree = 0 #Get out of jail free cards
        self.houses = 0 #Used for chance card calculation more than anything
        self.hotels = 0 #Used for chance card calculation more than anything
        self.doubles = 0 #How many doubles in a row they have rolled

def startGame(): #Game setupd
    print("Welcome to scuffed Monopoly!")
    global playercount, playing
    while True: #Loop input until a usable one is given
        playercount = input("How many people are playing? (2-6)\n> ")
        try:
            playercount = int(playercount) #This catches if input is not an int
        except:
            print("Invalid input! Please enter a number between 2 and 6!")
        else:
            if (playercount > 1 and playercount <= 6): #If number is valid
                break #Stop
            else:
                print("Invalid number! Please enter a number between 2 and 6!")
    for i in range(playercount): #Initialize players
        name = input(f"Player {i+1}'s name? > ")
        name = Player(name)
        playerlist.append(name)
    playing = True #Game loop runs while playing = True

def endGame(player):
    global playing
    print(f"{player.name} went bankrupt!") #Announce loser
    playing = False #
    input() #temp measure to prevent console closing on loss
    #planning on implementing a post-game restart

def turnOptions(player):
    print("What would you like to do?") #Print out the player's options
    options = ["Options: ", "Roll (r)", ", View Assets (v)"]
    inputOptions = ["r","v"]
    if player.jailed > 0:
        options.append(", Pay $50 to get out of Jail (p)") #Add pay option
        inputOptions.append("p")
        options[1] = "Attempt to roll doubles to get out of jail (d)" #Switch roll to roll doubles
        inputOptions[0] = "d" #switch r to d in checked input
    if len(player.propertyGroups) > 0: #if player has any full groups
        options.append(", Build houses/hotels (b)") #allows building of house/hotel
        inputOptions.append("b")
    for x in options:
        print(x, end="")
    print("")

    while True: #Loop to get the input from the player
        response = input("> ")
        if response in inputOptions:
            if response == "r": #Roll
                return "roll" #go to rolling and moving
            elif response == "v": #View Assets
                print(f"Current balance: ${player.money}")
                print("Owned properties: ", end=" ")
                for property in player.ownedProperties:
                    print(f"{property.name}", end=", ")
                print("\n")
                return turnOptions(player)
            elif response == "p": #Pay your way out of jail
                if payJail(player): #If they can  pay the $50, it does
                    player.jailed = 0
                    return "roll" #Go to rolling and moving
                else:
                    print("You remain in jail.")
                    #Could inlcude dice roll here, don't think I will
                return
            elif response == "d": #Attempt to roll Doubles
                attemptDoubles(player)
                #Moving after doubles attempt is handled by attemptDoubles()
                #May move parts back here for consistency
                return
            elif response == "b": #Build Houses/Hotels
                #buildHouses(player) #Not made yet
                print("Not implemented yet! How did you even access this?")
                turnOptions()
        else:
            print("Invalid input!")

def rollDice():
    print("Rolling dice...")
    global dice1, dice2, diceSum
    dice1, dice2 = randint(1,6), randint(1,6)
    print(f"You rolled a {dice1} and a {dice2}!")
    diceSum = dice1+dice2

def checkDoubles(player):
    if dice1 == dice2:
        player.doubles += 1
        if player.doubles == 3:
            print("Since you rolled doubles three consecutive times, you get sent to jail!")
            goJail(player)
            return "jail"
    else:
        player.doubles = 0

def movePlayer(player, diceSum):
    print(f"You move {diceSum} spaces.")
    player.position += diceSum
    if player.position >= 39:
        player.position -= 39
        player.money += 200
    print(f"You land on {propertylist[player.position].name}.")
    propertylist[player.position].land(player)

def payJail(player):
    if player.money < 50:
        print("You don't have enough money to pay to get out of Jail!")
        return False
    else:
        print("You paid $50 to get out of jail.")
        player.money -= 50
        return True

def attemptDoubles(player):
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
                player.jailed = 0
                movePlayer(player, diceSum)
        else:
            player.jailed -= 1
            print("You remain in jail.")

startGame() #Call game setup function
while playing: #Game loop
    for i in range(playercount): #Each player gets a turn
        player = playerlist[i] #Current player
        print(f"\n{player.name}'s turn.\n")

        if turnOptions(player) == "roll": #Rolling and moving only when player chooses that
            print("")
            rollDice()
            if checkDoubles(player) == "jail":
                continue
            movePlayer(player, diceSum)

        if playing == False: #If game ends, exit game loop
            break
