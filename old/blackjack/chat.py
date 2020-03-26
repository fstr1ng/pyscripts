#!/usr/bin/python3.7

import socket

hostname = socket.gethostname()
port = 0 # Zero is for any free port on system

def createServer(hostname, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((hostname, port))
    server.listen(5)
    return server

async def awaitConnections(server):
    welcomeMessage = 'Welcome to BlackJack at {}:{}. \n'.format(hostname, server.getsockname())
    welcomeMessage += 'Please enter your name: '

    clientSocket, clientAddress = server.accept()
    print(f"Connection from {clientAddress} has been established.")

    clientSocket.send(bytes(welcomeMessage, "utf-8"))
    playerName = clientSocket.recv(1024).decode('utf-8')

    return Player(playerName, [], clientSocket, clientAddress)

def runServer():
    server = createServer(hostname, port)


runServer()