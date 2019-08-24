import os 
import shutil

for p in range(4):
	for c in range(4):
		d_path = 'res/chapters/'+str(p)+'_'+str(c)+'/dialogs/'
		for f in os.listdir(d_path):
			os.remove(os.path.join(d_path,f))
		for f in os.listdir('res/dialogs/'):
			if '.txt' in f:
				try:
					if int(f[0])-1 == p and int(f[2])-1 == c:
						shutil.copy(os.path.join('res/dialogs/',f),os.path.join(d_path,str(f[4])+'.txt'))
				except:
					print('[*] Exception f:',f)