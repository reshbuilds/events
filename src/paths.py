
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))

RAW_PATH = os.path.join(project_path, 'data', 'raw')

if not os.path.exists(RAW_PATH):
    os.makedirs(RAW_PATH,exist_ok=True)

