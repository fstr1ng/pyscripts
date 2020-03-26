#!/usr/bin/python3.6

import random
import socket
import string
import sys

### CONFIG ###

hostname = socket.gethostname()
port = 6633

###################
### CLIENT PART ###
###################

if sys.argv[1] == 'c':
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.connect((hostname, port))

	welcomeMessage = serverSocket.recv(1024).decode("utf-8")
	print(welcomeMessage)

	myName = input()
	serverSocket.send(bytes(myName, "utf-8"))

	quit()

###################
### SERVER PART ###
###################

### CLASSES ###

class Card(object):
	def __init__(self, suit, rank, value):
		self.suit = suit
		self.rank = rank
		self.value = value

		self.name = '{} of {}'.format(self.rank, self.suit)
		
	def __repr__(self):
		return self.name

class Deck(object):
	def __init__(self):
		self.cards = []
		self.build()

	def __repr__(self):
		s = ''
		for card in self.cards:
			s += str(card) + '\n'
		return '{} card(s) in deck:\n'.format(len(self.cards)) + s 

	def build(self):
		for suit in 'Diamonds ♦;Clubs ♣; Hearts ♥;Spades ♠'.split(';'):
			for rank in 'Ace 2 3 4 5 6 7 8 9 10 Jack Queen King'.split():
				if rank in string.digits:
					value = int(rank)
				elif rank == 'Ace': 
					value = 11
				else:
					value = 10
				
				self.cards.append(Card(suit, rank, value))

	def shuffle(self):
		random.shuffle(self.cards)

class Player(object):
	def __init__(self, name, hand, socket, adress):
		self.name = name
		self.hand = hand
		self.socket = socket
		self.adress = adress
		self.score = 0
		self.countScore()

	def __repr__(self):
		s = ''
		for card in self.hand:
			s += str(card) + '\n'
		return 'Player {} score: {}\n'.format(self.name, self.score) + s  

	def countScore(self):
		self.score = sum([c.value for c in self.hand if c.rank != 'Ace'])

		aces = [c for c in self.hand if c.rank == 'Ace']

		if self.score <= 10 and len(aces) == 1:
			self.score += 11

		if self.score > 10:
			self.score += len(aces)

		if self.score < 10 and len(aces) >= 1:
			self.score += 11 + len(aces) - 1

	def addCard(self, card):
		self.hand.append(card)
		self.countScore()


### NETWORK PART ###

def createServer(hostname, port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((hostname, port))
	server.listen(5)
	return server

def awaitPlayer(server):
	welcomeMessage = 'Welcome to BlackJack at {}:{}. \n\
Please enter your name: '.format(hostname, port)

	clientSocket, clientAddress = server.accept()
	print(f"Connection from {clientAddress} has been established.")

	clientSocket.send(bytes(welcomeMessage, "utf-8"))
	playerName = clientSocket.recv(1024).decode('utf-8')

	return Player(playerName, [], clientSocket, clientAddress)

server = createServer(hostname, port)
print("Listening on " + str(port) + " at " + hostname)

player = awaitPlayer(server)

# clientSocket, clientAddress = acceptConnection(server)
# print(f"Connection from {clientAddress} has been established.")

# welcomeMessage = 'Welcome to BlackJack at {}:{}. \n\
# Please enter your name: '.format(hostname, port)

# clientSocket.send(bytes(welcomeMessage, "utf-8"))

# playerName = clientSocket.recv(1024).decode('utf-8')



### GAME SETUP ###

deck = Deck()
deck.shuffle()

player.addCard(deck.cards.pop())
player.addCard(deck.cards.pop())

dealer = Player('Dealer', [deck.cards.pop(), deck.cards.pop()], None, None)


print(player)
print(dealer)