import os
def keep(path):
	dir = os.listdir(path)
	if len(dir) == 0:
		f = open(os.path.join(path,'.keep'),'w')
		f.close()
	for d in dir:
		if os.path.isdir(os.path.join(path,d)):
			keep(os.path.join(path,d))
	
keep('./')