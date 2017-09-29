from utilities import *
import os

class Player:
    name = ""
    score = 0
    wins = 0
    was_winner = 0
    biggest = 0
    strike = 0
    biggest_strike = 0
    guess = -1
    took = -1

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 0
        self.wins = 0
        self.strike = 0
        self.guess = -1
        self.took = -1
        self.biggest = -1
        self.longest = 0
        self.biggest_strike = 0

    class PlayerLabel:
        def __init__(self, master, text, color, side=TOP):
            self.num = text
            self.label = Label(master, text=text, bg=color, fg=FG, font=FONT)
            self.label.config(font=("Courier", 20))
            self.label.pack(side=side, expand=1, fill=X)

    def printplayer(self, master):
        self.PlayerLabel(master, self.print(), self.color, LEFT)

    def print(self):
        s = self.name + "\n"
        if self.score >= 10 or self.score < 0:
            s += " "
        if self.score >= 100:
            s += " "
        s += " score: " + str(self.score) + "\n"
        s += "  wins: " + str(self.wins) + "\n" + "strike: " +\
            str(self.strike)
        return s

    def printguess(self, master):
        s = self.name + "\n"
        if self.score >= 10 or self.score < 0:
            s += " "
        if self.score >= 100:
            s += " "
        s += "score: " + str(self.score) + "\n"
        s += " wins: " + str(self.wins) + "\n"
        if int(self.guess) >= 10:
            s += " "
        s += "guess: " + str(self.guess)
        self.PlayerLabel(master, s, self.color, LEFT)

    def updatestrike(self):
        if self.biggest_strike < self.strike:
            self.biggest_strike = self.strike


def setnames():
    i = 0
    for entry in entries:
        player = Player(entry.get(), colors[i])
        players.append(player)
        i = i + 1


def playersort():
    for i in range(len(players)):
        temp = players[i]
        index = i
        for j in range(len(players) - i):
            if int(players[j + i].score) > int(temp.score):
                temp = players[j + i]
                index = j + i
        temp = players[i]
        players[i] = players[index]
        players[index] = temp


def playerupdatescore():
    score = 0
    for player in players:
        if int(player.guess) == int(player.took):
            score = int(player.took)*int(player.took) + 10
            player.wins += 1
            player.strike += 1

            # set biggest
            if int(player.guess) > int(player.biggest):
                player.biggest = player.guess
        if int(player.guess) < int(player.took):
            score = int(player.took)
            player.strike = 0

        if int(player.guess) > int(player.took):
            score = int(player.took) - int(player.guess)
            player.strike = 0

        player.updatestrike()
        player.score += score

        # set longest
        if player.strike > player.longest:
            player.longest = player.strike


def biggestwin():
    j = 0
    for i in range(len(players)):
        if int(players[i].biggest) > int(players[j].biggest):
            j = i
    return j


def biggeststrike():
    j = 0
    for i in range(len(players)):
        if int(players[i].biggest_strike) > int(players[j].biggest_strike):
            j = i
    return j


def mostwins():
    j = 0
    for i in range(len(players)):
        if int(players[i].wins) > int(players[j].wins):
            j = i
    return j


def sortarr():
    for i in range(len(players)):
        places[i] = i
    for i in range(len(players) - 1):
        temp = players[places[i]]
        index = places[i]
        for j in range(len(players) - i):
            if int(players[places[j + i]].score) > int(temp.score):
                temp = players[places[j + i]]
                index = j + i
        temp_index = places[i]
        places[i] = places[index]
        places[index] = temp_index

