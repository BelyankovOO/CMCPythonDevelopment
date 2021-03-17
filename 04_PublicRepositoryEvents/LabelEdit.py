import tkinter as tk

class Application(tk.Frame):nqw
	def __init__(self, master=None, title="InputLabel", **kwargs):
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
		self.labelText = InputLabel(self) 
		self.labelText.grid(sticky="nsew")

		self.buttonQuit = tk.Button(self, text = "Quit", command = self.master.quit)
		self.buttonQuit.grid()

class InputLabel(tk.Label):
	def __init__(self, master = None):
		self.letter = tk.StringVar()
		super().__init__(master, cursor = "xterm", relief = "sunken", font=("Courier", 14), takefocus=1, textvariable=self.letter, anchor=tk.W, highlightthickness=1)
		self.strip = tk.Frame(self, background="black", height=16, width=1)
		self.strip_place = 0
		self.strip.place(x=self.strip_place,y=1)

		self.hide_strip = False

		def hide_strip():
			if self.hide_strip == True:
				self.strip.configure(background=self.master['background'])
				self.hide_strip = False
			else:
				self.strip.configure(background="black")
				self.hide_strip = True
			self.master.after(500, hide_strip)

		hide_strip()

		self.bind('<Key>', self.key_clicked)
		self.bind('<Button-1>', self.mouse_clicked)


	def key_clicked(self, event):
		if event.keysym == "Right": 
			self.change_strip_position(self.strip_place+1)
		elif event.keysym == "Left": 
			self.change_strip_position(self.strip_place-1)
		elif event.keysym == "Home":
			self.change_strip_position(0)
		elif event.keysym == "End":
			self.change_strip_position(len(self.letter.get()))
		elif event.keysym == 'BackSpace':
			if self.strip_place > 0:
				self.letter.set(self.letter.get()[:self.strip_place-1]+self.letter.get()[self.strip_place:])
				self.change_strip_position(self.strip_place-1)	
		elif event.char:				
			self.letter.set(self.letter.get()[:self.strip_place]+event.char+self.letter.get()[self.strip_place:])
			self.change_strip_position(self.strip_place+1)

	def mouse_clicked(self, event):
		self.focus_set()
		self.change_strip_position(event.x//8)

	def change_strip_position(self, position):
		if position > len(self.letter.get()):
			return
		self.strip_place = position
		self.strip.place(x=self.strip_place*8+1, y=1)
						
app = Application()
app.mainloop()

