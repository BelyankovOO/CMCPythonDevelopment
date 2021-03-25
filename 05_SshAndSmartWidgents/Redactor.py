import tkinter as tk

class Application(tk.Frame):

    def __init__(self, master=None, title="<application>", **kwargs):
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        pass

class App(Application):
    def create_widgets(self):
        super().create_widgets()
        self.TextFrame = tk.Frame(self)
        self.TextFrame.grid(row=0, column=0)
        self.CanvasFrame = tk.Frame(self)
        self.CanvasFrame.grid(row=0, column=1)
        self.Q = tk.Button(self, text="Quit", command=self.master.quit)
        self.Q.grid(row=1, column=2)
        self.S1 = tk.Button(self, text="BuildByText", command=self.synchronizeByText)
        self.S1.grid(row=1, column=0)
        self.S2 = tk.Button(self, text="BuildByCanvas", command=self.synchronizeByCanvas)
        self.S2.grid(row=1, column=1)
        self.known_names = ["oval"]
        self.createTextFrame()
        self.createCanvasFrame()   

    def createTextFrame(self):
        self.TextRedactor = tk.Text(self.TextFrame, undo=True, background="#E4E4E4", relief="ridge", borderwidth="4")
        self.TextRedactor.grid(sticky="NEWS")
        self.TextRedactor.tag_config("error", background="firebrick1")

    def createCanvasFrame(self):
        self.CanvasRedactor = tk.Canvas(self.CanvasFrame, relief="ridge", background="#E4E4E4", borderwidth="4", takefocus=1)
        self.CanvasRedactor.grid(sticky="NEWS")
        self.CanvasRedactor.tag_click = False
        self.CanvasRedactor.bind('<Button-1>', self.canvasClick)
        self.CanvasRedactor.bind('<Motion>', self.changeSizeOrMove)                        

    def synchronizeByText(self):
        self.CanvasRedactor.delete("all")
        theText = self.TextRedactor.get('1.0', 'end-1c').split('\n')
        for i, line in enumerate(theText):
            if line == "":
                continue
            name, *paramenters = line.split()
            if name in self.known_names:
                self.TextRedactor.tag_remove("error", f"{i+1}.0", f"{i+1}.end")
                try:
                    eval(f"self.CanvasRedactor.create_{name}({','.join(paramenters)})")
                except:
                    self.TextRedactor.tag_add("error", f"{i+1}.0", f"{i+1}.end")
            else:
                self.TextRedactor.tag_add("error", f"{i+1}.0", f"{i+1}.end") 

    def synchronizeByCanvas(self):
        self.TextRedactor.delete('1.0', tk.END)
        for id in self.CanvasRedactor.find_all():
            stringToInsert = str(self.CanvasRedactor.type(id)) + " " \
            + str(self.CanvasRedactor.coords(id)[0]) + " " \
            + str(self.CanvasRedactor.coords(id)[1]) + " " \
            + str(self.CanvasRedactor.coords(id)[2]) + " " \
            + str(self.CanvasRedactor.coords(id)[3]) + " " \
            + "outline=" + "\"" + str(self.CanvasRedactor.itemcget(id, "outline")) + "\""  + " " \
            + "width=" + "\"" + str(self.CanvasRedactor.itemcget(id, "width")) + "\""  +" " \
            + "fill=" + "\""  +str(self.CanvasRedactor.itemcget(id, "fill")) + "\"" + "\n"
            self.TextRedactor.insert("end", stringToInsert)           

    def canvasClick(self, event):
        if len(self.CanvasRedactor.find_overlapping(event.x, event.y, event.x, event.y)) == 0:
            self.CanvasRedactor.tag_click = False
            self.oval = self.CanvasRedactor.create_oval(event.x, event.y, event.x, event.y, fill="blue", tags="check")
            self.coordinate = (event.x, event.y)
        else:
            self.oval = self.CanvasRedactor.find_overlapping(event.x, event.y, event.x, event.y)[-1]  
            self.coordinate = (event.x, event.y)
            self.CanvasRedactor.tag_click = True          
                    
    def changeSizeOrMove(self, event):
        if not self.CanvasRedactor.tag_click:
            if event.state == 0x0100:
                if event.x < self.CanvasRedactor.winfo_width()-4 and event.x > 4 and event.y < self.CanvasRedactor.winfo_height()-4 and event.y > 4:
                    self.CanvasRedactor.coords(self.oval, self.coordinate[0], self.coordinate[1], event.x, event.y)     
        else:
            if event.state == 0x0100:
                self.CanvasRedactor.move(self.oval, event.x-self.coordinate[0], event.y-self.coordinate[1])
                self.coordinate = (event.x, event.y)     

                        
app = App(title="Redactor")
app.mainloop()