from player import *
from utilities import *
from table import *

BG = "#3f3f3f"
FG = "white"
round_number = 1


class Game:
    def __init__(self):
        self.num = 0
        self.round_number = 0
        self.welcome = Game.Welcome(self)
        self.round = Game.Round(self)

    class StartTable:
        def __init__(self, master):
            self.frame = Frame(master, bg=BG)
            self.frame.pack(expand=1, fill=BOTH)

    class BridgeFrame:
        def __init__(self, text="Welcome To Bridge Emulator\n\n"):
            self.top = Game.StartTable(root)
            self.table = Game.StartTable(root)
            self.label = Label(self.top.frame, text=text, bg=BG, fg=FG)
            self.label.config(font=("Courier", 52))
            self.label.pack(expand=1, fill=X, side=TOP)

    class Welcome(BridgeFrame):
        def __init__(self, parent):
            Game.BridgeFrame.__init__(self)
            self.parent = parent
            self.label1 = Label(self.top.frame, text="How Many Players Will Play?", bg=BG, fg=FG)
            self.label1.config(font=("Courier", 44))
            self.label1.pack(expand=1, fill=X, side=TOP)
            self.button2 = self.NumButton(self, self.table.frame, "Two", BLUE, LEFT)
            self.button3 = self.NumButton(self, self.table.frame, "Three", PURPLE, LEFT)
            self.button4 = self.NumButton(self, self.table.frame, "Four", GREEN, LEFT)
            self.table.frame.mainloop()
            self.table.frame.destroy()
            self.top.frame.destroy()

        def getnum(self, num):
            if num == "Two":
                num = 2
            if num == "Three":
                num = 3
            if num == "Four":
                num = 4
            self.parent.num = int(num)
            self.destroylabels()
            self.getdata()

        def destroywelcome(self):
            for it in self.top.frame.pack_slaves():
                it.destroy()
            for it in self.table.frame.pack_slaves():
                it.destroy()

        def destroylabels(self):
            self.label1.destroy()
            self.button2.button.destroy()
            self.button3.button.destroy()
            self.button4.button.destroy()

        def getdata(self, e=0):
            self.label.config(text="Please Enter Players Name")
            self.label.update()
            for i in range(self.parent.num):
                entry = Entry(self.top.frame, bg=ENTRY_BG)
                entry.config(font=("Courier", 25))
                entry.pack(side=LEFT, expand=1, ipady=10)
                entries.append(entry)
            ok = self.parent.NextButton(self, self.table.frame, "Let's Go!", "green")
            ok.button.bind('<Button-1>', self.mainsetnames)

        def mainsetnames(self, event):
            setnames()
            self.destroywelcome()
            self.table.frame.quit()
            self.top.frame.quit()

        def destroyget(self):
            for entry in entries:
                entry.destroy()
            buttons = self.table.frame.pack_slaves()
            for b in buttons:
                b.destroy()
            self.label.config(text="")

        class NumButton:
            def __init__(self, parent, master, text, color, side=TOP):
                self.parent = parent
                self.num = text
                self.button = Button(master, text=text, bg=color, fg=FG, font=FONT, command=lambda: parent.getnum(text))
                self.button.config(font=("Courier", 20))
                self.button.pack(side=side, expand=1, fill=X, ipady=10)

    class NextButton:
        def __init__(self, parent, master, text="Next Round", color="Green", side=TOP):
            self.parent = parent
            self.round = round_number
            self.button = Button(master, text=text, bg=color, fg=FG, font=FONT, command=lambda: self.parent.nextround)
            self.button.config(font=("Courier", 20))
            self.button.pack(side=side, expand=1, fill=X, ipady=10)

    class Round(BridgeFrame):
        def __init__(self, parent):
            roundt = "Round Number " + str(round_number)
            Game.BridgeFrame.__init__(self, roundt)
            self.parent = parent
            self.i = 0
            self.sum = 0
            self.printscore()

        def printscore(self):
            sortarr()
            if self.parent.round_number == 0:
                text = "Let Us Start"
            else:
                text = "Round Number " + str(self.parent.round_number + 1)
            if self.parent.round_number == 13:
                text = "Round Number 13"
            self.label.config(text=text)
            for i in range(len(players)):
                players[places[i]].printplayer(self.top.frame)
            next_b = "Next"
            if self.parent.round_number == 13:
                next_b = "Finish"
            nextb = Game.NextButton(self, self.table.frame, next_b, "Green", RIGHT)
            nextb.button.bind('<Button-1>', self.nextround)
            nextb.button.bind_class("Button", "<Key-space>", self.nextround)
            nextb.button.mainloop()

        def cleanboard(self):
            for it in self.table.frame.pack_slaves():
                it.destroy()
            for it in self.top.frame.pack_slaves():
                if it != self.label:
                    it.destroy()

        def cleantop(self):
            for it in self.top.frame.pack_slaves():
                if it != self.label:
                    it.destroy()

        def nextround(self, event=0):
            self.parent.round_number = self.parent.round_number + 1
            self.cleanboard()
            if self.parent.round_number >= 14:
                self.finish()
            self.getguess()

        def getguess(self, event=0):
            self.cleantop()
            place = (self.parent.round_number - 1 + self.i) % self.parent.num
            self.label.config(text="Round " + str(self.parent.round_number) + "\n\n" +
                                   players[place].name + "\n"
                                   + "Please Enter Your Guess", fg=FG)
            if self.i + 1 == self.parent.num and self.parent.round_number >= self.sum:
                text = "Can't Say: " + str(self.parent.round_number - self.sum)
                label = Label(self.top.frame, text=text, fg="red", bg=BG, font=("Courier", 20))
                label.pack()
            entry = Entry(self.top.frame, font=("Courier", 44), bg=ENTRY_BG)
            entry.pack()
            entry.bind('<Return>', self.saveguess)
            entries[place] = entry

        def saveguess(self, event=0):
            place = (self.parent.round_number - 1 + self.i) % self.parent.num
            players[place].guess = entries[place].get()
            self.sum += int(entries[place].get())
            self.label.config(text="")
            entries[place].destroy()
            players[place].printguess(self.table.frame)
            self.i = self.i + 1
            if self.i == self.parent.num:
                self.i = 0
                self.showguess()
            self.getguess()

        def getscores(self, e=0):
            self.cleanboard()
            place = (self.parent.round_number - 1 + self.i) % self.parent.num
            self.label.config(text=players[place].name + "\n\n"
                                   + "Please Enter Your Score", fg=FG)
            entry = Entry(self.top.frame, font=("Courier", 44), bg=ENTRY_BG)
            entry.pack()
            entry.bind('<Return>', self.uptadescore)
            entries[place] = entry
            self.label.mainloop()

        def uptadescore(self, event=0):
            place = (self.parent.round_number - 1 + self.i) % self.parent.num
            players[place].took = entries[place].get()
            self.label.config(text="")
            entries[place].destroy()
            self.i = self.i + 1
            if self.i == self.parent.num:
                self.i = 0
                self.sum = 0
                playerupdatescore()
                self.printscore()
            self.getscores()

        def showguess(self):
            self.cleanboard()
            self.label.config(text="Round Number " + str(self.parent.round_number), fg=FG)
            for player in players:
                player.printguess(self.top.frame)
            next_b = "Next"
            if self.parent.round_number >= 14:
                next_b = "Finish"
            nextb = Game.NextButton(self, self.table.frame, next_b, "Green", RIGHT)
            nextb.button.bind('<Button-1>', self.getscores)
            nextb.button.bind_class("Button", "<Key-space>", self.getscores)
            nextb.button.mainloop()

        def finish(self):
            self.cleanboard()
            self.label.config(text="Final Scores:")
            self.printfinish()

        def printfinish(self):
            playersort()
            for player in players:
                player.printplayer(self.top.frame)
            self.winner()
            self.biggestwin()
            self.mostwins()
            self.bigeststrike()
            self.table.frame.mainloop()

        def winner(self):
            winner = players[0]
            text = "\nThe Winner Is: " + winner.name + "  ->  " + str(winner.score)
            winl = Label(self.table.frame, text=text, bg=BG, fg=winner.color)
            winl.config(font=("Courier", 34))
            winl.pack(anchor="w")

        def biggestwin(self):
            winner = biggestwin()
            text = "The Biggest Win Was Performed By: " + players[winner].name + "  ->  " + str(players[winner].biggest)
            winl = Label(self.table.frame, text=text, bg=BG, fg=players[winner].color)
            winl.config(font=("Courier", 34))
            winl.pack(anchor="w")

        def bigeststrike(self):
            winner = biggeststrike()
            text = "The Biggest Strike Was Performed By: " + players[winner].name + "  ->  " + \
                   str(players[winner].biggest_strike)
            winl = Label(self.table.frame, text=text, bg=BG, fg=players[winner].color)
            winl.config(font=("Courier", 34))
            winl.pack(anchor="w")

        def mostwins(self):
            winner = mostwins()
            text = "The Player Who Won The Most Rounds is: " + players[winner].name + "  ->  " + \
                   str(players[winner].wins)
            winl = Label(self.table.frame, text=text, bg=BG, fg=players[winner].color)
            winl.config(font=("Courier", 34))
            winl.pack(anchor="w")


root = Tk()
root.title("Bridge")
game = Game()
root.mainloop()


