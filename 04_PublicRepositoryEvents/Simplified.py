import tkinter as tk
import re 

def parser(parameter):
    gravity = "NEWS"
    row_weigth = 1
    row_heigth = 0
    column_weigth = 1
    column_width = 0 
    split1 = re.split(r':|/', parameter) 
    if len(split1) == 3: 
        gravity = split1[2]
    split2 = re.split(r'\+', split1[0])
    if len(split2) == 2:
        row_heigth = split2[1]    
    split3 = re.split(r'\.', split2[0])
    if len(split3) == 2:
        row_weigth = split3[1]
    split4 = re.split(r'\+', split1[1])
    if len(split4) == 2:
        column_width = split4[1]    
    split5 = re.split(r'\.', split4[0])
    if len(split5) == 2:
        column_weigth = split5[1]    
    return (split3[0], row_weigth, row_heigth, split5[0], column_weigth, column_width, gravity)  

class Application(tk.Frame):
    def __init__(self, master=None, title="Simlified",**kwargs):
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.createWidgets()

    def __getattr__(self, name):
        if name in dir(self):
            return dir[name]
        self.control = name    
        return self.widgetConstructor

    def widgetConstructor(self, obj, parameter, **kwargs):

        class InternalClass(obj):
            def __getattr__(self, name):
                if name in dir(self):
                    return self[name]
                self.control = name       
                return self.widgetConstructor  

            def widgetConstructor(self, obj, parameter, **kwargs):
                instance = obj(self, kwargs)
                setattr(self, self.control, instance)
                coordinate = parser(parameter)
                instance.master.rowconfigure(coordinate[0], weight = coordinate[1])
                instance.master.columnconfigure(coordinate[3], weight = coordinate[4])
                instance.grid(row=coordinate[0], column=coordinate[3], rowspan=str(int(coordinate[2])+1), columnspan=str(int(coordinate[5])+1), sticky=coordinate[6])

        instance = InternalClass(self, kwargs)
        setattr(self, self.control, instance)
        coordinate = parser(parameter)
        instance.master.rowconfigure(coordinate[0], weight = coordinate[1])
        instance.master.columnconfigure(coordinate[3], weight = coordinate[4])
        instance.grid(row=coordinate[0], column=coordinate[3], rowspan=str(int(coordinate[2])+1), columnspan=str(int(coordinate[5])+1), sticky=coordinate[6])

    def createWidgets():
        pass    

class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))

app = App(title="Simplified")
app.mainloop()