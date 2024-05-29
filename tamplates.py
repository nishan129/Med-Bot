import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname")

list_files = [
    "src/__init__.py",
    "src/prompt.py",
    "src/helper.py",
    ".env",
    "setup.py",
    "app.py",
    "store_index.py",
    "static",
    "templates/index.html"
]


for file_path in list_files:
    filepath = Path(file_path)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"creating directory : {filedir} for the file : {filename}")
        
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        
        logging.info(f"Creating empty file : {filepath}")
        
    else:
        logging.info(f"{filename} file is already exists")