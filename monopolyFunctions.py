def goJail(player): #This doesn't belong :(
    if player.jailfree == 0:
        player.jailed = 3
    else:
        player.jailfree -= 1
    player.position = 10

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

def collectfromall(player, amount):
    for i in range(playercount):
        playerlist[i].money -= amount
    player.money += (amount * playercount)
