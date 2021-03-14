import copy
import tkinter as tk
from tkinter import messagebox as mb
import random

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=3)
        self.master.grid_columnconfigure(0, weight=1)

        self.upperFrame = tk.Frame(self.master, background="red")
        self.upperFrame.grid(row=0, column=0, sticky="nsew")
        self.createUpperFrame()

        self.mainFrame = tk.Frame(self.master, background="white")
        self.mainFrame.grid(row=1, column=0, sticky="nsew")
        self.createMainFrame()

    def createUpperFrame(self):
        self.upperFrame.grid_columnconfigure(0, weight=1)
        self.upperFrame.grid_columnconfigure(1, weight=1)
        self.upperFrame.grid_rowconfigure(0, weight=1)

        self.timeButton = tk.Button(self.upperFrame, text='New', command=self.newGameStart)
        self.quitButton = tk.Button(self.upperFrame, text='Quit', command=self.quit)
    
        self.timeButton.grid(row=0, column=0, sticky="nsew")
        self.quitButton.grid(row=0, column=1, sticky="nsew")

    
    def createMainFrame(self):
        c = 1
        self.buttonsArray = []
        for i in range(4):
            self.mainFrame.grid_columnconfigure(i, weight=1)
            self.mainFrame.grid_rowconfigure(i, weight=1)
            self.buttonsArray.append([])
            for j in range(4):
                if i == 3 and j == 3: 
                    self.buttonsArray[i].append("empty")
                else:    
                    self.buttonsArray[i].append(tk.Button(self.mainFrame, text=c, command=self.buttonListener(i,j)))
                    c+=1            
        self.newGameStart()        

    def newGameStart(self):
        dic = {}
        for i in range(len(self.buttonsArray)):
            for x in self.buttonsArray[i]:
                dic.setdefault(type(x), []).append(x)
        buff = sorted(dic[tk.Button], key = lambda butt: int(butt['text']))
        c = 0
        for i in range(4):
            for j in range(4):
                if i == 3 and j == 3:
                    self.buttonsArray[i][j] = "empty"
                else:
                    self.buttonsArray[i][j] = buff[c]
                    c += 1 
        random.shuffle(self.buttonsArray)#убрать для проверки на победу                           
        self.updateBoard()

    def buttonListener(self,i,j):
            return lambda: self.buttonClicked(i,j)

    def buttonClicked(self,i,j):
        self.moving(i,j)
        if self.winningCheck():
            self.showWinningMessage()
            self.newGameStart()
        self.updateBoard()

    def winningCheck(self):
        for i in range(4):
            for j in range(4):
                if type(self.buttonsArray[i][j]) != str:
                    if int(self.buttonsArray[i][j]['text']) != i*4+(j+1):
                        return False
        return True            
        

    def showWinningMessage(self):
        mb.showinfo(title="Congratulation", message="You win!!!")        

    def moving(self,i,j):
        if j-1 >= 0:
            if self.buttonsArray[i][j-1] == "empty":
                empty = self.buttonsArray[i][j-1]
                self.buttonsArray[i][j-1] = self.buttonsArray[i][j]
                self.buttonsArray[i][j] = empty
        if j+1 <= 3:
            if self.buttonsArray[i][j+1] == "empty":
                empty = self.buttonsArray[i][j+1]
                self.buttonsArray[i][j+1] = self.buttonsArray[i][j]
                self.buttonsArray[i][j] = empty
        if i-1 >= 0:
            if self.buttonsArray[i-1][j] == "empty":
                empty = self.buttonsArray[i-1][j]
                self.buttonsArray[i-1][j] = self.buttonsArray[i][j]
                self.buttonsArray[i][j] = empty
        if i+1 <= 3:
            if self.buttonsArray[i+1][j] == "empty":
                empty = self.buttonsArray[i+1][j]
                self.buttonsArray[i+1][j] = self.buttonsArray[i][j]
                self.buttonsArray[i][j] = empty         
             
    def updateBoard(self):
        for i in range(4):
            for j in range(4):
                if type(self.buttonsArray[i][j]) != str: 
                    self.buttonsArray[i][j].configure(command=self.buttonListener(i,j))
                    self.buttonsArray[i][j].grid(row=i, column=j, sticky="nsew")


app = Application()
app.master.title('15')
app.mainloop()
