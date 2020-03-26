#!/usr/bin/python3.6
import socket

hostname = socket.gethostname()
port = 6633

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((hostname, port))

welcomeMessage = serverSocket.recv(1024).decode("utf-8")
print(welcomeMessage)

myName = input()
serverSocket.send(bytes(myName, "utf-8"))