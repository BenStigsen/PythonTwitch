from re import search as regex
import socket
import commands, configurator

def sendMessage(message):
    s.send(f"PRIVMSG #{CHAN} :{message}\r\n".encode("utf-8"))

def sendRaw(data):
    s.send(f"{data}\r\n".encode("utf-8"))

    if "PASS" in data:
        data = f"data[5:]{'*'*30}"

    print(f"[RAW DATA] {data}")

def recvMessage(username, message):
    print(f"[MESSAGE] {username}: {message}")

def recvCommand(username, command):
    print(f"[COMMAND] {username}: {command}")

def recvIRC(data):
    print(f"[IRC DATA] {data}")

credentials = configurator.load("credentials.json")
AUTH = credentials["AUTH"]
NICK = credentials["NICK"]
CHAN = credentials["CHAN"].lower()
 
s = socket.socket()
s.connect(("irc.chat.twitch.tv", 6667))

sendRaw(f"PASS {AUTH}")
sendRaw(f"NICK {NICK}")
sendRaw(f"JOIN #{CHAN}")
print(f"Joined #{CHAN}")

prefix = "!"

run = True

while run:
    data = s.recv(2048).decode("utf-8")

    if data == "PING :tmi.twitch.tv\r\n":
        recvIRC(data)
        sendRaw("PONG :tmi.twitch.tv")

    elif "PRIVMSG" in data:
        match = regex(r"^:(\w+)!.* :(.+)", data)

        username = match[1].strip()
        message  = match[2].strip()

        if message[0] == prefix:
            recvCommand(username, message)
            response = commands.handleCommands(username, message)

            if response:
                sendMessage(response)

                if response == "/disconnect":
                    run = False

        else:
            recvMessage(username, message)

    else:
        recvIRC(data)