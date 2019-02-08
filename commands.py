def handleCommands(username, message):
	commands = {
		"ping"		:ping,
		"hello"		:hello,

		"dc"		:disconnect,
		#"command"	:function,
	}

	cmd = message[1:].split(" ", 1)[0].strip()

	if cmd in commands:
		return commands[cmd](username, message)
	else:
		return None

def ping(username, *args):
	return f"Pong! {username}"

def hello(username, *args):
	return f"Hello {username}!"

def disconnect(username, *args):
	moderators = ["tearzz"]

	if username in moderators:
		return f"/disconnect"