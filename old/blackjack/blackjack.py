#!/usr/bin/python3.6

import argparse
import random
import socket
import string
import sys

### CLI ARGUMENTS ###

parser = argparse.ArgumentParser(prog='blackjack')
parser.add_argument("-s", "--server", help="Server mode", action='store_true')

args = parser.parse_args()

### CONFIG ###

hostname = socket.gethostname()
port = 0 # Zero is for any free port on system

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
        for suit in '♦ Diamonds;♣ Clubs;♥ Hearts;♠ Spades'.split(';'):
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


### NETWORK FUCTIONS ###

def createServer(hostname, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((hostname, port))
    server.listen(5)
    return server

def awaitPlayer(server):
    welcomeMessage = 'Welcome to BlackJack at {}:{}. \n'.format(hostname, server.getsockname())
    welcomeMessage += 'Please enter your name: '

    clientSocket, clientAddress = server.accept()
    print(f"Connection from {clientAddress} has been established.")

    clientSocket.send(bytes(welcomeMessage, "utf-8"))
    playerName = clientSocket.recv(1024).decode('utf-8')

    return Player(playerName, [], clientSocket, clientAddress)

### GAME LOOPS ###

def runServer():
    server = createServer(hostname, port)
    print("Listening on " + str(server.getsockname()) + " at " + hostname)
    player = awaitPlayer(server)

    deck = Deck()
    deck.shuffle()

    player.addCard(deck.cards.pop())
    player.addCard(deck.cards.pop())

    dealer = Player('Dealer', [deck.cards.pop(), deck.cards.pop()], None, None)

    print(player)
    print(dealer)

def runClient():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((hostname, port))

    welcomeMessage = serverSocket.recv(1024).decode("utf-8")
    print(welcomeMessage)

    myName = input()
    serverSocket.send(bytes(myName, "utf-8"))
    quit()

def main():
    if args.server:
        runServer()
    else:
        runClient()

if __name__ == '__main__':
    main()
