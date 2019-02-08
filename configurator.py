import json

def load(cfg_file):
	with open(cfg_file) as f:
		settings = json.load(f)

	return settings