import os

def r(**args):
	print("[*] In dirlister module")
	return str(os.listdir("."))