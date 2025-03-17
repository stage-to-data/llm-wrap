import llmwrap
import os
import shutil

temp_dest = os.path.join(os.getcwd(), "temp")
if os.path.isdir(temp)

# Get prompt:
prompot_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "describe.txt")
image_source = os.path.join(os.getcwd(), "examples", "tutorial", "assets", "moleman.jpeg")
prompt = llmwrap.Prompt(prompot_source, images = [image_source])

shutil.rmtree(temp_dest)