
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
print(project_path)

RAW_PATH = os.path.join(project_path, 'data', 'raw')
print(RAW_PATH)

if not os.path.exists(RAW_PATH):
    os.makedirs(RAW_PATH,exist_ok=True)

