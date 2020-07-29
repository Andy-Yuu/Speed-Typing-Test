import tkinter
import requests

class typingTestGUI:
	def __init__(self):

		# creates main gui
		self.main_window = tkinter.Tk()

		# variable to hold and display random words
		self.currentWord = tkinter.StringVar()
		self.displayWords = tkinter.StringVar()

		# creates frame for current and display message widget
		self.topFrame = tkinter.Frame(self.main_window)
		self.bottomFrame = tkinter.Frame(self.main_window)

		# countdown timer 
		self.countdown = 60

		# creates componenets
		self.current = tkinter.Message(self.topFrame, textvariable = self.currentWord, width = 500)
		self.display = tkinter.Message(self.topFrame, textvariable = self.displayWords, width = 500)
		self.entry = tkinter.Entry(self.bottomFrame)
		self.start = tkinter.Button(self.bottomFrame, text = "start" , command = lambda: self.startClock(self.countdown))
		self.timer = tkinter.Label(self.bottomFrame, text = 60)

		self.current.config(fg = 'green')

		# listens to keyboard inputs with callback
		self.entry.bind("<Key>", self.keyListener)

		# current word
		word = requests.get("https://random-word-api.herokuapp.com/word?number=1")
		self.currentWord.set(word.json()[0])

		# gets random words from api and displays them
		self.newWord = requests.get("https://random-word-api.herokuapp.com/word?number=5")
		self.displayWord0 = self.newWord.json()[0]
		self.displayWord1 = self.newWord.json()[1]
		self.displayWord2 = self.newWord.json()[2]
		self.displayWord3 = self.newWord.json()[3]
		self.displayWord4 = self.newWord.json()[4]

		self.displayWords.set(self.displayWord0 + " " + self.displayWord1 + " " + self.displayWord2 + " " + self.displayWord3 + " " + self.displayWord4)

		# packs frame componenets 
		self.topFrame.pack()
		self.bottomFrame.pack()
		self.current.pack(side = "left")
		self.display.pack(side = "right")
		self.entry.pack()
		self.start.pack()
		self.timer.pack()
		

		# initializes variables
		self.entryString = ""
		self.bool = 1
		self.charactersTyped = 0


		# enter gui infinite loop until closed
		tkinter.mainloop()

	# starts countdown and calculates gross wpm
	def startClock(self, time):
		self.timer["text"] = time

		if (time > 0):
			self.main_window.after(1000, self.startClock, time - 1)
		if (time == 0): 
			wpm = self.charactersTyped / 5
			self.timer["text"] = "Gross Words Per Minute {}".format(wpm)



	def keyListener(self, key):
		# space bar to go to next word and clear entry
		if (key.keycode == 32):

			# clears the entry widget
			self.entry.delete(0, 'end')

			# resets string to nothing and bool to true
			self.entryString = ""
			self.bool = 1

			# calls changeWords to update current word
			self.changeWords(key)

		else: 
			# tests whether the input matches the current word
			self.bool = self.isMatching(key)

		# displays red if they mispelt the word, blue if theyre typing it correctly
		if (self.bool == 1):
			self.current.config(fg = "green")
		else:
			self.current.config(fg = "red")

	def isMatching(self, key):

		# backspace will delete last character
		if (key.keycode == 3342463):
			self.entryString = self.entryString[:-1]
		else:
			self.charactersTyped = self.charactersTyped + 1
			self.entryString = self.entryString + key.char

		lengthString = len(self.entryString)

		# creates temp word from current word to match with entry string
		tempCurrentWord = ""
		for i in range(0,lengthString):
			tempCurrentWord = tempCurrentWord + self.currentWord.get()[i]

		# tests to see if they match
		try:
			if (self.entryString == tempCurrentWord):
				return 1
			else:
				return 0
		# if indexing out of bounds it means they are not spelling the word correctly, so just return 0
		except IndexError:
			return 0

	# updates current word and gets new word
	def changeWords(self, key):
		tempWord = requests.get("https://random-word-api.herokuapp.com/word?number=1")
		self.currentWord.set(self.displayWord0)

		self.displayWord0 = self.displayWord1
		self.displayWord1 = self.displayWord2
		self.displayWord2 = self.displayWord3
		self.displayWord3 = self.displayWord4
		self.displayWord4 = tempWord.json()[0]

		self.displayWords.set(self.displayWord0 + " " + self.displayWord1 + " " + self.displayWord2 + " " + self.displayWord3 + " " + self.displayWord4)

gui = typingTestGUI()













