import subprocess

subprocess.call("python object_table_parser.py", shell=True)
subprocess.call("python object_content_distributor.py", shell=True)
subprocess.call("python map_images_distributor.py", shell=True)
subprocess.call("python synthesis_table_parser.py", shell=True)
subprocess.call("python unlock_table_parser.py", shell=True)
subprocess.call("python dialog_distributor.py", shell=True)
subprocess.call("python npc_distributor.py", shell=True)
subprocess.call("python switching_scene_table_parser.py", shell=True)
subprocess.call("python puzzle_table_parser.py", shell=True)